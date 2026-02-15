from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.services.feature_engineering import FeatureEngineer
from app.services.risk_detection import PCOSRiskDetector
from app.services.explainable_ai import ExplainableAI
from app.services.remedy_engine import RemedyEngine
from app.services.report_generator import ReportGenerator
import json

router = APIRouter()

# Initialize services
feature_engineer = FeatureEngineer()
risk_detector = PCOSRiskDetector()
explainable_ai = ExplainableAI()
remedy_engine = RemedyEngine()
report_generator = ReportGenerator()

@router.post("/analyze", response_model=schemas.AssessmentResponse)
async def analyze_assessment(
    assessment_input: schemas.AssessmentInput,
    db: Session = Depends(get_db)
):
    """
    Main endpoint for PCOS risk assessment
    Processes input data and returns risk assessment with phenotype
    """
    try:
        # Step 1: Feature Engineering
        input_dict = assessment_input.dict()
        features = feature_engineer.engineer_features(input_dict)
        
        # Step 2: Risk Detection
        risk_assessment = risk_detector.detect_risk(features, taken_birth_control=input_dict.get('taken_birth_control_pills', False))
        
        # Step 3: Explainable AI - Get key drivers
        key_drivers = explainable_ai.calculate_feature_importance(
            features,
            risk_assessment['risk_score'],
            risk_assessment['phenotype']
        )
        
        # Step 4: Generate explanation
        explanation = explainable_ai.generate_explanation(
            features,
            risk_assessment['risk_level'],
            risk_assessment['phenotype'],
            risk_assessment['risk_score'],
            risk_assessment['confidence_score']
        )
        
        # Step 5: Get personalized remedies
        remedies_list = remedy_engine.get_combined_remedies_list(
            risk_assessment['phenotype'],
            risk_assessment['risk_level']
        )
        
        # Step 6: Get clinical next steps
        next_steps = remedy_engine.get_clinical_next_steps(
            risk_assessment['risk_level']
        )
        
        # Step 7: Save to database
        try:
            db_assessment = models.Assessment(
                **input_dict,
                risk_level=risk_assessment['risk_level'],
                phenotype=risk_assessment['phenotype'],
                confidence_score=risk_assessment['confidence_score'],
                risk_score=risk_assessment['risk_score'],
                key_drivers=key_drivers,
                feature_values=features,
                shap_values={"explanation": explanation}
            )
            db.add(db_assessment)
            db.commit()
            db.refresh(db_assessment)
        except Exception as db_error:
            db.rollback()
            error_msg = str(db_error)
            if "taken_birth_control_pills" in error_msg or "column" in error_msg.lower() or "no such column" in error_msg.lower():
                detail = "Database schema error: The 'taken_birth_control_pills' column is missing. Please run 'python init_db.py' to update the database tables."
            else:
                detail = f"Database error: {error_msg}. Please check server logs."
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detail
            )
        
        # Prepare response
        response = schemas.AssessmentResponse(
            risk_level=risk_assessment['risk_level'],
            phenotype=risk_assessment['phenotype'],
            confidence=f"{risk_assessment['confidence_score'] * 100:.0f}%",
            risk_score=risk_assessment['risk_score'],
            key_drivers=key_drivers,
            remedies=remedies_list,
            next_steps=next_steps,
            assessment_id=db_assessment.id
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error processing assessment: {error_trace}")
        
        error_msg = str(e)
        if "taken_birth_control_pills" in error_msg or "column" in error_msg.lower():
            detail = f"Database schema error: {error_msg}. Please run 'python init_db.py' to update the database tables."
        else:
            detail = f"Error processing assessment: {error_msg}"
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

@router.get("/{assessment_id}", response_model=schemas.AssessmentResult)
async def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a saved assessment by ID
    """
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Get remedies and next steps
    remedies_list = remedy_engine.get_combined_remedies_list(
        assessment.phenotype,
        assessment.risk_level
    )
    next_steps = remedy_engine.get_clinical_next_steps(assessment.risk_level)
    
    return schemas.AssessmentResult(
        id=assessment.id,
        created_at=assessment.created_at,
        risk_level=assessment.risk_level,
        phenotype=assessment.phenotype,
        confidence_score=assessment.confidence_score,
        risk_score=assessment.risk_score,
        key_drivers=assessment.key_drivers or [],
        remedies=remedies_list,
        next_steps=next_steps,
        disclaimer="This is not a medical diagnosis. Please consult a doctor for confirmation."
    )

@router.get("/{assessment_id}/report")
async def download_report(assessment_id: int, db: Session = Depends(get_db)):
    """
    Generate and download PDF report for an assessment
    """
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Get remedies and next steps
    remedies_dict = remedy_engine.get_remedies(assessment.phenotype, assessment.risk_level)
    next_steps = remedy_engine.get_clinical_next_steps(assessment.risk_level)
    
    # Prepare report data
    report_data = {
        'risk_level': assessment.risk_level,
        'phenotype': assessment.phenotype,
        'confidence_score': assessment.confidence_score,
        'risk_score': assessment.risk_score,
        'key_drivers': assessment.key_drivers or [],
        'remedies': remedies_dict,
        'next_steps': next_steps,
        'explanation': assessment.shap_values.get('explanation', '') if assessment.shap_values else ''
    }
    
    # Generate PDF
    pdf_bytes = report_generator.generate_pdf(report_data)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ovasense_report_{assessment_id}.pdf"
        }
    )

@router.get("/user/{user_id}/history")
async def get_user_history(user_id: str, db: Session = Depends(get_db)):
    """
    Get assessment history for a user
    """
    assessments = db.query(models.Assessment).filter(
        models.Assessment.user_id == user_id
    ).order_by(models.Assessment.created_at.desc()).all()
    
    results = []
    for assessment in assessments:
        results.append({
            'id': assessment.id,
            'created_at': assessment.created_at,
            'risk_level': assessment.risk_level,
            'phenotype': assessment.phenotype,
            'risk_score': assessment.risk_score,
            'confidence_score': assessment.confidence_score
        })
    
    return {"assessments": results}


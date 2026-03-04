from typing import Annotated, List
from fastapi import APIRouter, Request, Header, Form, Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/v1"
)

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/patients", response_model=LungCancerResponse)
async def create_patient(
    patient: LungCancerCreate,
    db: AsyncSession = Depends(get_db)
):
    new_patient = LungCancer(**patient.model_dump())
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient

# =========================
# GET ALL WITH FILTER + PAGINATION
# =========================

@router.get("/patients", response_model=List[LungCancerResponse])
async def get_patients(
    skip: int = 0,
    limit: int = Query(100, le=500),
    gender: Optional[str] = None,
    lung_cancer: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(LungCancer)

    if gender:
        query = query.where(LungCancer.gender == gender)

    if lung_cancer is not None:
        query = query.where(LungCancer.lung_cancer == lung_cancer)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

# =========================
# GET BY ID
# =========================

@router.get("/patients/{patient_id}", response_model=LungCancerResponse)
async def get_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LungCancer).where(LungCancer.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient

# =========================
# UPDATE
# =========================

@router.put("/patients/{patient_id}", response_model=LungCancerResponse)
async def update_patient(
    patient_id: int,
    updated: LungCancerCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LungCancer).where(LungCancer.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in updated.model_dump().items():
        setattr(patient, key, value)

    await db.commit()
    await db.refresh(patient)

    return patient

# =========================
# DELETE
# =========================

@router.delete("/patients/{patient_id}")
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LungCancer).where(LungCancer.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    await db.delete(patient)
    await db.commit()

    return {"message": "Deleted successfully"}

# =========================
# ANALYTICS ENDPOINTS FOR PENTAHO
# =========================

@router.get("/analytics/cancer-rate")
async def cancer_rate(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(func.avg(LungCancer.lung_cancer))
    )
    avg_value = result.scalar()

    return {
        "cancer_rate_percentage": round(avg_value * 100, 2)
    }

@router.get("/analytics/by-gender")
async def cancer_by_gender(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            LungCancer.gender,
            func.avg(LungCancer.lung_cancer)
        ).group_by(LungCancer.gender)
    )

    rows = result.all()

    return [
        {
            "gender": row[0],
            "cancer_rate_percentage": round(row[1] * 100, 2)
        }
        for row in rows
    ]

@router.get("/analytics/age-distribution")
async def age_distribution(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            LungCancer.age,
            func.count()
        ).group_by(LungCancer.age)
    )

    return [
        {"age": row[0], "count": row[1]}
        for row in result.all()
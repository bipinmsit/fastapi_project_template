from sqlalchemy.orm import Session
from models.models import StaticStage, Page, Workflow,Mail,Document,Exception
from postgres.database import Session_Local
from utils.config.logger import logger
from schemas.schemas import MailBase, StageBase, StageOut, PageBase, PageOut, WorkflowBase, WorkflowOut,DocumentBase,ExceptioBase


def create_stage(db: Session, data: StageBase):

    try:
        doc = StaticStage(**data)
        db.add(doc)
        db.commit()
        return doc

    except Exception as e:
        logger.error("An error occurred while creating the stage:", str(e))
        raise  # Re-raise the exception for further handling
    
def get_stages(db: Session):
    stages = db.query(StaticStage).all()
    return stages
    
    
    
def create_mail(db: Session, data: MailBase):
    
    doc = Mail(**data)
    db.add(doc)
    db.commit()
    return doc

def create_page(db: Session, data: PageBase):
    
    doc = Page(**data)
    db.add(doc)
    db.commit()
    return doc

def create_workflow(db: Session, data: WorkflowBase):
    
    
    doc = Workflow(**data)
    db.add(doc)
    db.commit()
    if doc:
        return True
    else:
        return False


def get_pkstage(db: Session, stage):
    stage_obj = db.query(StaticStage).filter(StaticStage.stage_name==stage).first()
    return stage_obj

def get_pk_mail(db:Session,email_uuid):
    tbl_email_obj = db.query(Mail).filter(Mail.pk_email_uuid == email_uuid).first()
    return tbl_email_obj

def update_mail(email_uuid: str, updates: dict,db):
    # Find the existing mail entry
    existing_mail = db.query(Mail).filter(Mail.pk_email_uuid == email_uuid).first()
    
    if not existing_mail:
        return 

    # Update fields based on provided dictionary
    for key, value in updates.items():
        if hasattr(existing_mail, key) and value is not None:
            setattr(existing_mail, key, value)

    db.commit()
    db.refresh(existing_mail)
    
    return existing_mail


def create_document(db: Session, data: DocumentBase):
    
    doc = Document(**data)
    db.add(doc)
    db.commit()
    return doc

def create_exception(db: Session, data:ExceptioBase):
    obj = Exception(**data)
    db.add(obj)
    db.commit()
    return obj





    
    
    
    
    
    
    
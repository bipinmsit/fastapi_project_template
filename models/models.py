import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,JSON,Text
from models.base_model import RequiredField
from sqlalchemy.dialects.postgresql import ARRAY

class Mail(RequiredField):   
    __tablename__ = 'tbl_mail'
    
    pk_email_uuid = Column(String(256), unique=True, index=True, nullable=False,primary_key=True)
    usermail = Column(String(50))
    fk_curr_stage_id = Column(Integer,ForeignKey('tbl_static_stage.pk_stage_id'))
    fk_prev_stage_id =Column(Integer,ForeignKey('tbl_static_stage.pk_stage_id'))
    email_outlook_id = Column(String(256), unique=True, index=True, nullable=False)
    email_queue_message_id = Column(String(256), unique=True, index=True)
    retry_count = Column(Integer, default=0)
    subject = Column(String(256),nullable=True)
    quote_details = Column(JSON,nullable=True)
    is_archive = Column(Integer, default=0)

class StaticStage(RequiredField):
    
    __tablename__ = 'tbl_static_stage'
    pk_stage_id = Column(Integer, primary_key=True, index=True)
    stage_name = Column(String(100), unique=True)
    
class Document(RequiredField):
    
    __tablename__ = 'tbl_document'
    pk_document_id = Column(String(50), primary_key=True, default=lambda:str(uuid.uuid4()),index=True)
    doc_name = Column(String(100),nullable=True)
    fk_mail_id = Column(String(256),ForeignKey('tbl_mail.pk_email_uuid'))

    
    
class Page(RequiredField):
    
    __tablename__ = 'tbl_page'
     
    pk_page = Column(String(50), primary_key=True, default=lambda:str(uuid.uuid4()),index=True)
    page_name = Column(String(100),nullable=True)
    fk_doc_id = Column(String(50),ForeignKey('tbl_document.pk_document_id'))
    uploaded_folder_path = Column(String(100),nullable=True)

class Workflow(RequiredField):
    __tablename__ = 'tbl_workflow'
    
    pk_workflow = Column(String(50), primary_key=True, default=lambda:str(uuid.uuid4()),index=True)
    fk_mail_id = Column(String(256),ForeignKey('tbl_mail.pk_email_uuid'))
    reason_stage_change = Column(String(100),nullable=True)
    transition_stage_id = Column(Integer,ForeignKey('tbl_static_stage.pk_stage_id'))
    
class Exception(RequiredField):
    __tablename__ = 'tbl_exception'
    
    pk_exception = Column(String(50), primary_key=True, default=lambda:str(uuid.uuid4()),index=True)
    fk_mail_id = Column(String(256),ForeignKey('tbl_mail.pk_email_uuid'))
    message = Column(Text,nullable=True)

class Document(RequiredField):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    embedding = Column(ARRAY(float), nullable=False)
    
    
    
    
    
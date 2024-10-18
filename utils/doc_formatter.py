from datetime import datetime
from typing import List
from xml.etree.ElementTree import Element, tostring

from docx import Document
from docx.text.paragraph import Paragraph
from docx.opc.part import Part
from docx.opc.constants import RELATIONSHIP_TYPE, CONTENT_TYPE
from docx.opc.oxml import parse_xml
from docx.opc.packuri import PackURI
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

document_comment_counters = {}   # keep track of comment counters per document

class DocumentFormatter:
    def __init__(self, doc_object, author):
        """
        Initialize the formatter with an existing Word document object and the author.
        
        :param doc_object: An existing Word document object (from python-docx).
        :param author: Name of the author for document comments.
        """
        self.document = doc_object  # Assign the existing document object
        self.author = author
        self.doc_id = id(doc_object)
        self.comment_id_counter = 0 # initialize a comment counter
        self.base_xml = "<comments></comments>"  # Base XML structure for comments

        # initialize the comment counter for this document if it is not already done 
        if self.doc_id not in document_comment_counters:
            document_comment_counters[self.doc_id]=0
        
        self._COMMENTS_PART_DEFAULT_XML_BYTES = (
            b"""
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r
        <w:comments
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            xmlns:o="urn:schemas-microsoft-com:office:office"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:w10="urn:schemas-microsoft-com:office:word"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
            xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
            xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"
            xmlns:lc="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas"
            xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"
            xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
            xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
            xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml"
            xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex"
            xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid"
            xmlns:cr="http://schemas.microsoft.com/office/comments/2020/reactions">
        </w:comments>
        """
        ).strip()


    @classmethod
    def from_doc_name(cls, doc_name, author):
        """
        Alternate constructor to create a new DocumentFormatter using a document name.
        
        :param doc_name: The file name or path of the Word document to open.
        :param author: Name of the author for document comments.
        :return: An instance of DocumentFormatter.
        """
        doc_object = Document(doc_name)  # Load the document from file
        return cls(doc_object, author)  # Use the regular constructor

    @classmethod
    def create_new_document(cls, author):
        """
        Alternate constructor to create a new Word document.
        
        :param author: Name of the author for document comments.
        :return: An instance of DocumentFormatter with a new blank document.
        """
        doc_object = Document()  # Create a new blank document
        return cls(doc_object, author)

    def get_next_comment_id(self):
        # Generate the next unique comment Id for this document
        document_comment_counters[self.doc_id] +=1
        return(str(document_comment_counters[self.doc_id]))
    
    def save(self, output_name):
        """
        Save the Word document with a new name.
        
        :param output_name: The name to save the Word document as.
        """
        self.document.save(output_name)



    def add_comment( self, para: Paragraph,  comment_text: str
    ) -> None:
        if  para is None:
            return
        
        # set up the underlying element
        element=para._element
        
        #generate a unique ID for the new comment
        comment_id  = self.get_next_comment_id()
        print(f"comment_id:{comment_id}")
        try:
            comments_part = self.document.part.part_related_by(
                RELATIONSHIP_TYPE.COMMENTS
            )
        except KeyError:
            comments_part = Part(
                partname=PackURI("/word/comments.xml"),
                content_type=CONTENT_TYPE.WML_COMMENTS,
                blob=self._COMMENTS_PART_DEFAULT_XML_BYTES,
                package=self.document.part.package,
            )
            self.document.part.relate_to(comments_part, RELATIONSHIP_TYPE.COMMENTS)

        comments_xml = parse_xml(comments_part.blob)
        # Create the comment
        #comment_id = str(len(comments_xml.findall(qn("w:comment"))))
        comment_element = OxmlElement("w:comment")
        comment_element.set(qn("w:id"), comment_id)
        comment_element.set(qn("w:author"), self.author)
        comment_element.set(qn("w:date"), datetime.now().isoformat())

        # Create the text element for the comment
        comment_paragraph = OxmlElement("w:p")
        comment_run = OxmlElement("w:r")
        comment_text_element = OxmlElement("w:t")
        comment_text_element.text = comment_text
        comment_run.append(comment_text_element)
        comment_paragraph.append(comment_run)
        comment_element.append(comment_paragraph)

        comments_xml.append(comment_element)
        comments_part._blob = tostring(comments_xml)

        # Create the commentRangeStart and commentRangeEnd elements
        comment_range_start = OxmlElement("w:commentRangeStart")
        comment_range_start.set(qn("w:id"), comment_id)
        comment_range_end = OxmlElement("w:commentRangeEnd")
        comment_range_end.set(qn("w:id"), comment_id)

        # Add the commentRangeStart to the first element and commentRangeEnd to
        # the last element
        # elements[0].insert(0, comment_range_start)
        # elements[-1].append(comment_range_end)

        element.insert(0, comment_range_start)
        element.append(comment_range_end)


        # Add the comment reference to each element in the range
        # for element in elements:
        comment_reference = OxmlElement("w:r")
        comment_reference_run = OxmlElement("w:r")
        comment_reference_run_properties = OxmlElement("w:rPr")
        comment_reference_run_properties.append(
            OxmlElement("w:rStyle", {qn("w:val"): "CommentReference"})
        )
        comment_reference_run.append(comment_reference_run_properties)
        comment_reference_element = OxmlElement("w:commentReference")
        comment_reference_element.set(qn("w:id"), comment_id)
        comment_reference_run.append(comment_reference_element)
        comment_reference.append(comment_reference_run)
        element.append(comment_reference)
        
        print("Added Comment to Document : ", comment_text)
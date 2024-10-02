from ast import arguments
import graphene
import base64
from graphene_sqlalchemy import SQLAlchemyObjectType
from model import MenuItem, Contact, Chef, db

class MenuItemType(SQLAlchemyObjectType):
    class Meta:
        model = MenuItem
        interfaces = (graphene.relay.Node,)

class ContactType(SQLAlchemyObjectType):
    class Meta:
        model = Contact
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    menu_items = graphene.List(MenuItemType)
    contacts = graphene.List(ContactType)

    def resolve_menu_items(self, info):
        return MenuItem.query.all()
    
    def resolve_contacts(self, info):  # Hàm để lấy danh sách contact
        return Contact.query.all()

class DeleteContact(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    # print(id)
    id_bytes = Arguments.id # Chuyển đổi đối tượng ID thành chuỗi
    # print(id_str)
    # decoded_bytes = base64.b64decode(id_str)
    # print(decoded_bytes)
    # id_bytes = decoded_bytes
    # # id_bytes = str(decoded_bytes)
    # # _,bytes_id = id_bytes.split(':')
    # print(bytes_id)
    # b = bytes(bytes_id, 'utf-8')
    # print(b)
    # id_actual = b.decode('utf-8')
    # print(id_bytes)
    # Giải mã ID từ Base64
    decoded_bytes = base64.b64decode(id_bytes)
    print(decoded_bytes)
    decoded_str = decoded_bytes.decode('utf-8')
    _, actual_id = decoded_str.split(':')
    print(actual_id)
        
    # Chuyển thành số nguyên

    def mutate(self, info, id_actual):
        #try:
            # Giả sử contact_id là một số nguyên, không cần giải mã
            #actual_id = int(id)
        #except ValueError:
        print(f"Invalid contact ID: {id_actual}")
            #return DeleteContact(success=False)
        contact = Contact.query.get(id_actual)
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return DeleteContact(ok=True)
        return DeleteContact(ok=False)

class Mutation(graphene.ObjectType):
    delete_contact = DeleteContact.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

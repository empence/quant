from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user, logout_user, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# TODO values for calculated columns could be broken by a change in ID numbering
# is this OK?? I haven't decided

# TODO you can only sort by one column , due to hackish way of storing sorts. 


app = Flask(__name__)

login = LoginManager(app)

app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@login.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


class User(UserMixin, db.Model):
    """
    Standard user mixin. 
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # a user ID
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    tables = db.relationship('VirtualTable', backref='users', lazy=True)


class VirtualRow(db.Model): 
    """
    Describes entries in a single row in a virtual table. 

    Virtual tables are things that the user might think of as just containing 
    their own data, but actually all the user data is stored together in the 
    same non-virtual table, and access is controlled when the data is accessed 
    or changed so the user cannot see the difference.  I did things this way
    because relational databases in general perform better with long tables than
    many tables - i.e. one per user-created table.  
    Each row of this table corresponds to an entry in some virtual table. 
    The virtual tables may have different numbers and column types, within the 
    constraints of: 
    # string columns < 10
    # float columns < 10
    # foreign key columns (referencing objects in other virtual tables) < 5
    # date-time columns < 5
    Columns not used in a given virtual table are just null. 
    I'd also like to point out that in this fallen world, you can implement a 
    Postgres table *with a Postgres table*.
    
    Properties: 
    id: Primary key. 
    virtual_table: The virtual table that this row goes in. 

    All other properties are the values this row has for various columns. 
    If a table simply doesn't use that column, then its value will be null. 
    """
    __tablename__ = "virtual_rows" 
    id = db.Column(db.Integer, primary_key=True)
    virtual_table = db.Column(db.Integer, db.ForeignKey('virtual_tables.id'), 
                                nullable=False)

    string_column1 = db.Column(db.String, nullable=True)
    string_column2 = db.Column(db.String, nullable=True)    
    string_column3 = db.Column(db.String, nullable=True)
    string_column4 = db.Column(db.String, nullable=True)
    string_column5 = db.Column(db.String, nullable=True)
    string_column6 = db.Column(db.String, nullable=True)
    string_column7 = db.Column(db.String, nullable=True)
    string_column8 = db.Column(db.String, nullable=True)
    string_column9 = db.Column(db.String, nullable=True)
    string_column10 = db.Column(db.String, nullable=True)
    float_column1 = db.Column(db.Float, nullable=True)
    float_column2 = db.Column(db.Float, nullable=True)
    float_column3 = db.Column(db.Float, nullable=True)
    float_column4 = db.Column(db.Float, nullable=True)
    float_column5 = db.Column(db.Float, nullable=True)
    float_column6 = db.Column(db.Float, nullable=True)
    float_column7 = db.Column(db.Float, nullable=True)
    float_column8 = db.Column(db.Float, nullable=True)
    float_column9 = db.Column(db.Float, nullable=True)
    float_column10 = db.Column(db.Float, nullable=True)
    # since all rows actually are stored in the same table, 
    # any "foreign keys" in the virtual table correspond to just other rows
    # in the underlying table. 
    foreign_key1 = db.Column(db.Integer, db.ForeignKey('virtual_rows.id'), 
                            nullable=True)
    foreign_key2 = db.Column(db.Integer, db.ForeignKey('virtual_rows.id'), 
                            nullable=True)
    foreign_key3 = db.Column(db.Integer, db.ForeignKey('virtual_rows.id'), 
                            nullable=True)
    foreign_key4 = db.Column(db.Integer, db.ForeignKey('virtual_rows.id'), 
                            nullable=True)
    foreign_key5 = db.Column(db.Integer, db.ForeignKey('virtual_rows.id'), 
                            nullable=True)
    datetime_column1 = db.Column(db.DateTime, nullable=True)
    datetime_column2 = db.Column(db.DateTime, nullable=True)
    datetime_column3 = db.Column(db.DateTime, nullable=True)
    datetime_column4 = db.Column(db.DateTime, nullable=True)
    datetime_column5 = db.Column(db.DateTime, nullable=True)


class VirtualTable(db.Model):
    """
    Describes a virtual table: its headings, name, and what user it belongs to. 

    Properties: 
    id: primary key
    name: Name of this table. 
    user: What user this table belongs to. 
    spreadsheet_views: Relationship object containing all the views this table
    has. 
    rows: Relationship object containing all the rows this table has. 

    All other properties represent the names of the corresponding columns in
    this virtual table. If a table doesn't use that column, then the value will
    be null. 
    """
    __tablename__="virtual_tables"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), 
                                nullable=False)
    spreadsheet_views = db.relationship('SpreadsheetView', 
                                        backref='virtual_tables', lazy=True)
    rows = db.relationship('VirtualRow',
                                        backref='virtual_tables', lazy=True)

    string_column1_name = db.Column(db.String, nullable=True)
    string_column2_name = db.Column(db.String, nullable=True)    
    string_column3_name = db.Column(db.String, nullable=True)
    string_column4_name = db.Column(db.String, nullable=True)
    string_column5_name = db.Column(db.String, nullable=True)
    string_column6_name = db.Column(db.String, nullable=True)
    string_column7_name = db.Column(db.String, nullable=True)
    string_column8_name = db.Column(db.String, nullable=True)
    string_column9_name = db.Column(db.String, nullable=True)
    string_column10_name = db.Column(db.String, nullable=True)
    float_column1_name = db.Column(db.String, nullable=True)
    float_column2_name = db.Column(db.String, nullable=True)
    float_column3_name = db.Column(db.String, nullable=True)
    float_column4_name = db.Column(db.String, nullable=True)
    float_column5_name = db.Column(db.String, nullable=True)
    float_column6_name = db.Column(db.String, nullable=True)
    float_column7_name = db.Column(db.String, nullable=True)
    float_column8_name = db.Column(db.String, nullable=True)
    float_column9_name = db.Column(db.String, nullable=True)
    float_column10_name = db.Column(db.String, nullable=True)
    foreign_key1_name = db.Column(db.String, nullable=True)
    foreign_key2_name = db.Column(db.String, nullable=True)
    foreign_key3_name = db.Column(db.String, nullable=True)
    foreign_key4_name = db.Column(db.String, nullable=True)
    foreign_key5_name = db.Column(db.String, nullable=True)
    datetime_column1_name = db.Column(db.String, nullable=True)
    datetime_column2_name = db.Column(db.String, nullable=True)
    datetime_column3_name = db.Column(db.String, nullable=True)
    datetime_column4_name = db.Column(db.String, nullable=True)
    datetime_column5_name = db.Column(db.String, nullable=True)

class SpreadsheetView(db.Model):
    """
    Describes a view on a particular virtual table: view name, columns shown, etc.

    The user doesn't really see the table in its entirety. The user sees views
    on that table, and those views can eliminate columns, move them around, sort
    by columns, or add columns that don't contain actual data, but are
    constructed from columns that do exist by a formula.
    This class describes one view the user can take on a table, including what
    constructed and non-constructed columns it has, and which one of them you
    should sort by. 
    Properties: 
    id: primary key
    name: The name of this view. 
    table: The table that this is a view of. 
    sort_by: What column this should be sorted by. 
    sort_ascending: Whether to sort that column in an ascending direction or not. 
    """
    __tablename__="spreadsheet_views"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    table = db.Column(db.Integer, db.ForeignKey('virtual_table.id'), 
                        nullable=False)
    spreadsheet_view_columns = db.relationship('SpreadsheetViewColumn', 
                                                backref='spreadsheet_views', 
                                                lazy=True)
    sort_by = db.Column(db.Integer, db.ForeignKey('spreadsheet_view_columns.id'), 
                        nullable=False)
    sort_ascending = db.Column(db.Boolean, nullable=False)


class SpreadsheetViewColumn(db.Model): 
    """ 
    Describes a column in a view spreadsheet - what it contains and where it goes.

    Properties: 
    id: Primary key. 
    num_within_view: An integer n, meaning that this column is the nth column
    from the left within this view. 
    calculated: Bool. Whether this contains an actual data value - a column in a 
    virtual table - or whether this column's value is calculated from a formula. 
    name is the name of the column. 
    value: The value of this column. If calculated is false, this will contain
    a table ID and column ID. Otherwise, it'll contain a formula using tableID
    and column ID pairs and operands, that will be evaulated to get this column's
    value. 
    name: The name of this spreadsheet column. 
    spreadsheet_view: The spreadsheet view this column is in. 

    I apologize for the fact that num_within_view is a property of a column, not
    a property of the view - I believe it's the least hackish way I could do it 
    within a standard database setup.
    """
    __tablename__="spreadsheet_view_columns"
    id = db.Column(db.Integer, primary_key=True)
    num_within_view = db.Column(db.Integer, nullable=False)
    calculated = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    spreadsheet_view = db.Column(db.Integer, db.ForeignKey('spreadsheet_views.id'), 
                                nullable=False)


@app.route('/')
def hello_world():
    return 'Hello, World!'
"""Run interactively using your own authorized account. No credentials are saved here."""
import wrds
with wrds.Connection() as db:
    libraries=[x for x in db.list_libraries() if 'crsp' in x.lower()]
    print('Entitled CRSP libraries:',libraries)
    library=input('Library to inspect (copy from list): ').strip()
    if library not in libraries:raise ValueError('Choose a listed library')
    tables=db.list_tables(library=library);print(tables)
    table=input('Table to inspect: ').strip()
    if table not in tables:raise ValueError('Choose a listed table')
    print(db.describe_table(library=library,table=table).to_string(index=False))
    print('Read field definitions before exporting. No return definition is inferred.')

import spacy

nlp = spacy.load('en_core_web_sm')

def extractEntities(doc):
    entities = []

    # Extract entities based on desired patterns or rules
    for token in doc:
        if token.pos_ == 'PROPN':
            entities.append({
                'var_name': token.text.lower().replace(' ', '_'),
                'type': 'string',
                'description': f'{token.text} entity'
            })

    return entities

def generateSQLQuery(entities):
    operation = input("Enter the SQL operation (e.g., SELECT, INSERT, UPDATE, DELETE): ")
    table = input("Enter the table name: ")
    conditions = []

    if operation.upper() == 'SELECT':
        columns = input("Enter the column names (comma-separated): ")
        query = f"SELECT {columns} FROM {table} WHERE "
        for entity in entities:
            var_name = entity['var_name']
            value = input(f"Enter the value for {var_name}: ")
            conditions.append(f"{var_name} = '{value}'")
    elif operation.upper() == 'INSERT':
        columns = input("Enter the column names (comma-separated): ")
        values = input("Enter the values (comma-separated): ")
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    elif operation.upper() == 'UPDATE':
        column = input("Enter the column name to update: ")
        new_value = input("Enter the new value: ")
        query = f"UPDATE {table} SET {column} = '{new_value}' WHERE "
        for entity in entities:
            var_name = entity['var_name']
            value = input(f"Enter the value for {var_name}: ")
            conditions.append(f"{var_name} = '{value}'")
    elif operation.upper() == 'DELETE':
        query = f"DELETE FROM {table} WHERE "
        for entity in entities:
            var_name = entity['var_name']
            value = input(f"Enter the value for {var_name}: ")
            conditions.append(f"{var_name} = '{value}'")
    else:
        print("Invalid SQL operation.")
        return None

    if conditions:
        query += " AND ".join(conditions)

    return query

def convertTextToSQL(text):
    doc = nlp(text)
    entities = extractEntities(doc)
    sqlQuery = generateSQLQuery(entities)

    return sqlQuery


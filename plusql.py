############################################################
#  Copyright(c) 2021  Denis Lussier.  All rights reserved. #
############################################################

import sqlalchemy

from sqlalchemy import create_engine

import sys, os

PROMPT="SQL> "


def main_loop():
  s_sql = load_sql_file(f_sql)

  stmt = ""
  line_num = 0
  stmt_line_num = 1
  for line in s_sql:
    line_num = line_num + 1

    if line == "" or line.startswith("--"):
      print(f"[{line_num}] {line}")
      continue

    if line.endswith(";"):
      stmt = stmt + line
      if stmt_line_num < line_num:
        stmt_line_num = line_num
      exec_sql(stmt, stmt_line_num)
      stmt = ""
      stmt_line_num = line_num + 1
    else:
      stmt = stmt + line + "\n"


def load_sql_file(p_f_sql):
  try:
    with open(p_f_sql) as f:
      s_sql = f.readlines()
  except Exception as e:
    print(e)
    sys.exit(1)
    
  s_sql  = [x.rstrip() for x in s_sql]
  return(s_sql)


def exec_sql(p_stmt, p_line_num):
  print_sql_stmt(p_stmt, p_line_num)

  ## figure out what to do by looking at the first token
  sp_stmt = p_stmt.split()
  for token in sp_stmt:
    l_token = token.lower()
    if l_token == "select":
      rc = execute_sql_select(p_stmt, p_line_num)
    else:
      rc = execute_sql(p_stmt, p_line_num)
    break

  return(rc)


def print_sql_stmt(p_sql, p_line_num):
  print(f"[{p_line_num}] {PROMPT} {p_sql.rstrip()}")


def execute_sql_select(p_stmt, p_line_num):
  try:
    result = con1.execute(p_stmt)
  except Exception as e:
    print_sql_exception(e, p_line_num)
    return(False)

  print_rows(result.fetchall())

  return(True)


def execute_sql(p_stmt, p_line_num):
  try:
    con1.execute(p_stmt)
  except Exception as e:
    print_sql_exception(e, p_line_num)
    return(False)
  return(True)


def print_rows(p_rows):
  if p_rows:
    print(str(p_rows))


def print_empty_line():
  print("")
  

def print_sql_exception(e, p_line_num=0):
    e_lines = str(e).split("\n")
    e_line = 0
    for line in e_lines:
      if line.startswith("(Background on this error at"):
        continue
      if line.startswith("[SQL: "):
        continue

      e_line = e_line + 1
      if e_line == 1 and p_line_num > 0:
        print(f"[ERROR near line {p_line_num}] {line}")
      else:
        print(line)


#############################################
## MAINLINE
#############################################

if (len(sys.argv) < 2):
  print("Invalid parameters")
  sys.exit(1)
f_sql = sys.argv[1]

eng1 = create_engine('sqlite:///:memory:')
con1 = eng1.connect()
main_loop()

sys.exit(0)

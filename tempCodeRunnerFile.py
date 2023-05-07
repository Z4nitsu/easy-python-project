   c.execute("""CREATE TABLE payroll (
        name text,
        employee_id integer,
        employer text,
        address text,
        weekly_work_hours integer,
        hourly_pay integer,
        monthly_pay integer
        )""")
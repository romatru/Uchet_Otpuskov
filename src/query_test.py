from dal import DAL

def demo():
    dal = DAL("vacations.db")

    print("Departments:", dal.list_departments())
    print("Employees before:", dal.list_employees())

    print("Requests (all):")
    for r in dal.list_requests():
        print(r)

    report = dal.generate_hr_report()
    print("HR report generated:", report)

    print("HR reports in DB:")
    for r in dal.list_hr_reports():
        print(r)

if __name__ == "__main__":
    demo()

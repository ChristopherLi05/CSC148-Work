"""CSC148 Prep 3: Inheritance

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu

=== Module Description ===
This module contains an illustration of *inheritance* through an abstract
Employee class that defines a common interface for all of its subclasses.

As usual, delete the TODO comments after you've completed each part.

There is also a task inside prep3_starter_tests.py.
Make sure to look at that file and complete the TODO there as well.
"""
from datetime import date
from python_ta.contracts import check_contracts


################################################################################
# Part 1
# In this part of the prep, you will implement the total_pay method of the
# Employee class.
#
# You may add new PRIVATE instance attributes to the class to help store a
# record of the payments. Private instance attributes are attributes whose
# names start with _ and should not be accessed by code outside of the class.
#
# Document any new attributes in your class docstring, include type annotations
# for them in the class body, and make sure you initialize them properly
# in the Employee.__init__ method. You can, and should, also update the
# Employee.pay method implementation to update your new attribute(s).
#
# You may assume as a precondition that the pay method is not called on the
# same employee twice in the same month.
#
# NOTE: You only need to change the Employee class, and you should NOT change
# its two subclasses (they will simply inherit the Employee.total_pay method).
################################################################################
@check_contracts
class Employee:
    """An employee of a company.

    This is an abstract class. Only child classes should be instantiated.

    Public Attributes:
    - id_: This employee's ID number.
    - name: This employee's name.

    Private Attributes: (add yours here)
    - _total_payment: The employee's total payment
    """
    id_: int
    name: str
    _total_payment: float

    def __init__(self, id_: int, name: str) -> None:
        """Initialize this employee.

        Note: This initializer is meant for internal use only;
        Employee is an abstract class and should not be instantiated directly.
        """
        self.id_ = id_
        self.name = name
        self._total_payment = 0

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        raise NotImplementedError

    def pay(self, pay_date: date) -> None:
        """Pay this Employee on the given date and record the payment.

        (Assume this is called at most once per month.)
        """
        payment = self.get_monthly_payment()
        self._total_payment += payment
        print(f'An employee was paid {payment} on {pay_date}.')

    def total_pay(self) -> float:
        """Return the total amount of pay this Employee has received.

        >>> e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
        >>> e.pay(date(2018, 6, 28))
        An employee was paid 100.0 on 2018-06-28.
        >>> e.pay(date(2018, 7, 28))
        An employee was paid 100.0 on 2018-07-28.
        >>> e.pay(date(2018, 8, 28))
        An employee was paid 100.0 on 2018-08-28.
        >>> e.total_pay()
        300.0
        """
        return self._total_payment


@check_contracts
class SalariedEmployee(Employee):
    """An employee whose pay is computed based on an annual salary.

    Public Attributes:
    - salary: This employee's annual salary

    Representation Invariants:
    - self.salary >= 0
    """
    id_: int
    name: str
    salary: float

    def __init__(self, id_: int, name: str, salary: float) -> None:
        """Initialize this salaried Employee.

        Preconditions:
        - salary >= 0

        >>> e = SalariedEmployee(14, 'Fred Flintstone', 5200.0)
        >>> e.salary
        5200.0
        """
        Employee.__init__(self, id_, name)
        self.salary = salary

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = SalariedEmployee(99, 'Mr Slate', 120000.0)
        >>> e.get_monthly_payment()
        10000.0
        """
        return round(self.salary / 12, 2)


@check_contracts
class HourlyEmployee(Employee):
    """An employee whose pay is computed based on an hourly rate.

    Public Attributes:
    - hourly_wage:
        This employee's hourly rate of pay.
    - hours_per_month:
        The number of hours this employee works each month.

    Representation Invariants:
    - self.hourly_wage >= 0
    - self.hours_per_month >= 0
    """
    id_: int
    name: str
    hourly_wage: float
    hours_per_month: float

    def __init__(self, id_: int, name: str, hourly_wage: float,
                 hours_per_month: float) -> None:
        """Initialize this HourlyEmployee.

        Preconditions:
        - hourly_wage >= 0
        - hours_per_month >= 0

        >>> barney = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> barney.hourly_wage
        1.25
        >>> barney.hours_per_month
        50.0
        """
        Employee.__init__(self, id_, name)
        self.hourly_wage = hourly_wage
        self.hours_per_month = hours_per_month

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> e.get_monthly_payment()
        62.5
        """
        return round(self.hours_per_month * self.hourly_wage, 2)


################################################################################
# Part 2
# In this part of the prep, you will implement the total_payroll method
# of the Company class.
#
# Do not add any additional instance attributes (public or private) to this class.
# You don't need to add any in order to complete this task!
################################################################################
@check_contracts
class Company:
    """A company with employees.

    We use this class mainly as a client for the various Employee classes
    we defined in employee.

    Public Attributes:
    - employees: the employees in the company.
    """
    employees: list[Employee]

    def __init__(self, employees: list[Employee]) -> None:
        """Initialize a new company."""
        self.employees = employees

    def pay_all(self, pay_date: date) -> None:
        """Pay all employees at this company."""
        for employee in self.employees:
            employee.pay(pay_date)

    def total_payroll(self) -> float:
        """Return the total of all payments ever made to all employees of this company.

        >>> my_corp = Company([
        ...     SalariedEmployee(24, 'Gilbert the cat', 1200.0),
        ...     HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)
        ... ])
        >>> my_corp.pay_all(date(2018, 6, 28))
        An employee was paid 100.0 on 2018-06-28.
        An employee was paid 500.25 on 2018-06-28.
        >>> my_corp.total_payroll()
        600.25
        """
        return sum(i.total_pay() for i in self.employees)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run prep3" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['datetime'],
        'allowed-io': ['Employee.pay'],
        'max-line-length': 100,
        "output-format": "python_ta.reporters.PlainReporter"
    })

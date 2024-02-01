import random
import pandas as pd
from typing import List, Dict
from src.utils import (
    select_from_list_by_decreasing_prob,
    generate_numericals,
)

class DataGenerator:
    def __init__(
        self,
        num_employees: int,
        projects: List[str],
        work_categories: List[str],
        departments: List[str],
        numericals: List[str],
        start_times: List[float] = [8, 7.5, 8.5],
        end_times: List[float] = [16, 17, 16.5],
        break_durations: List[int] = [0.5, 1, 0],
    ) -> None:
        self.num_employees = num_employees
        self.projects = projects
        self.work_categories = work_categories
        self.departments = departments
        self.numericals = numericals
        self.start_times = start_times
        self.end_times = end_times
        self.break_durations = break_durations
        self.reg_id_counter = 0

    def generate_data(self, start_date: str, end_date: str):
        """
        Generates a dataset and a dataframe of registrations for a given time period.
        """
        registrations: List[Dict] = self._generate_registrations(start_date, end_date)
        return registrations

    def _generate_registrations(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Generates registrations for each employee for each day between start_date and end_date
        """
        registrations: List[Dict] = []
        train_dates = pd.date_range(
            start=pd.to_datetime(start_date, format="%Y-%m-%d"),
            end=pd.to_datetime(end_date, format="%Y-%m-%d"),
        )
        for _date in train_dates:
            for employee in range(self.num_employees):
                emp_id = f"employee-{employee}"
                reg_id = f"reg-{self.reg_id_counter}"
                registrations.append(
                    self._create_reg(reg_id, emp_id, _date.strftime("%Y-%m-%d"))
                )
                self.reg_id_counter += 1
        return registrations

    def _create_reg(self, reg_id: str, employee_id: str, date: str):
        """
        Creates a registration for a given employee on a given date
        """
        start_time: float = select_from_list_by_decreasing_prob(self.start_times)
        end_time: float = select_from_list_by_decreasing_prob(self.end_times)
        break_duration: float = select_from_list_by_decreasing_prob(
            self.break_durations
        )
        work_duration: float = end_time - start_time - break_duration
        return {
            "registrationId": reg_id,
            "date": date,
            "employeeId": employee_id,
            "projectId": random.choice(self.projects),
            "departmentId": random.choice(self.departments),
            "workCategory": random.choice(self.work_categories),
            "startTime": start_time,
            "endTime": end_time,
            "workDuration": work_duration,
            "breakDuration": break_duration,
            "publicHoliday": False,
            "numericals": generate_numericals(self.numericals),
        }

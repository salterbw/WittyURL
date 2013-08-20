from django.db import models
from django.utils import timezone
import datetime

# A project model to keep track of all the projects I'm working on
class Project(models.Model):
    project_name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    start_date = models.DateField('Start Date: ')
    end_date = models.DateField('(Expected) Completion Date: ')
    project_url = models.URLField(blank = True) # This may be black since some repos are private
    is_completed = models.BooleanField() # To keep track of if the project is completed or not and should be treated accordingly
    
    # This makes sure if it is viewed as an object we see the project name
    def __unicode__(self):
        return self.project_name
    
    # This is used to organize the admin screen
    def was_completed(self):
        return self.is_completed
    was_completed.admin_order_field = 'end_date'
    was_completed.boolean = True
    was_completed.short_description = 'Has the project been completed yet?'
    
    # Returns True if the project is ending with a week
    # Meant to be used as a filter
    def is_ending_soon(self):
        return self.end_date <= timezone.now() + datetime.timedelta(days=7) and not self.is_completed
    
    # This is called to set a project as completed
    def complete_project(self):
        if not self.is_completed:
            self.end_date = timezone.now()
            self.is_completed = True
            
    
# Every project has a set of milestones indicating progress on the project
class Milestone(models.Model):
    project = models.ForeignKey(Project)
    milestone_name = models.CharField(max_length = 200)
    milestone_desc = models.CharField(max_length = 500)
    milestone_date = models.DateTimeField('Accomplished:')
    
    # This makes sure if it is viewed as an object we see the milestone name
    def __unicode__(self):
        return self.milestone_name
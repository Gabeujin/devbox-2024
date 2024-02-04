class Job:
    def __init__(self, skill, link, title, company_name, location, reward):
        self.skill = skill
        self.link = link 
        self.title = title
        self.company_name = company_name
        self.location = location
        self.reward = reward
    
    def intro(self):
        print(f"----------------------{self.skill}")
        print(f"Job: {self.title}\nCompany: {self.company_name}\nLocation: {self.location}\nReward: {self.reward}\nlink: {self.link}\n")

    def to_export_list(self):
        return [self.skill, self.link, self.title, self.company_name, self.location, self.reward]
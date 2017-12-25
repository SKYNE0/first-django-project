from django import forms
class UserForm(forms.Form):
    username = forms.CharField(label='账号:')
    password = forms.CharField(label='密码:', widget= forms.PasswordInput)


class UserInfoForm(forms.Form):
    username = forms.CharField(label='用户名:')
    password = forms.CharField(label='密码:',widget= forms.PasswordInput)
    job_num = forms.IntegerField(label='工号:')
    sex_choice = {('male', '男'), ('female', '女'), }
    job_choice = {('A', '普通员工'), ('B','记帐员'), ('C','仓库主管'),('D','统计员'),('E','保管员')}
    sex = forms.ChoiceField(label='性别:', choices= sex_choice)
    job = forms.ChoiceField(label='职位:', choices= job_choice)


class InfoChange(forms.Form):
    oldusername = forms.CharField(label='旧用户名:')
    oldpassword = forms.CharField(label='旧密码:',widget= forms.PasswordInput)
    username = forms.CharField(label='新用户名:')
    password = forms.CharField(label='新密码:',widget= forms.PasswordInput)
    sex_choice = {('male', '男'), ('female', '女'), }
    sex = forms.ChoiceField(label='性别:', choices= sex_choice)

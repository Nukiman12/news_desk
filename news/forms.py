from django import forms
from .models import News


# class NewsForm(forms.Form):
#     news = forms.CharField(max_length=150,label="название",widget=forms.TextInput(attrs={"class":"form-control"}))
#     description = forms.CharField(label="текст",widget=forms.Textarea(attrs={"class":"form-control"}))
#     is_published = forms.BooleanField(required=False, label="опубликовать", widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
#     Category = forms.ModelChoiceField(empty_label="choose category",label='категория',queryset=Category.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))




class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['news','description','content','is_published','Category']
        widgets = {
            "news": forms.TextInput(attrs={"class":"form-control"}),
            'description': forms.Textarea(attrs={"class":"form-control","rows":5}),
            'content': forms.Textarea(attrs={"class":"form-control","rows":10}),
            'is_published': forms.CheckboxInput(attrs={"class":"form-check-input"}),
            'Category': forms.Select(attrs={"class":"form-control"})
        }
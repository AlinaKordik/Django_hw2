from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Article, Tag, Scope


class ScopeFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Считаем количество форм, где отмечен is_main и форма не помечена на удаление
        main_categories_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('is_main'):
                main_categories_count += 1

        if main_categories_count != 1:
            raise ValidationError("У статьи должен быть один и только один основной раздел.")

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeFormSet
    extra = 4


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline,]
    exclude = ('tag', )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

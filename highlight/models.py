from django.db import models



class Xcourse(models.Model):
    course_name = models.TextField(max_length=100,default="")

    class Meta: 
        verbose_name = "xcourse"
        verbose_name_plural = "xcourse"
        ordering = ['course_name']

class Xlesson(models.Model):
    course = models.ForeignKey(Xcourse,on_delete=models.CASCADE)
    lesson_name = models.TextField(max_length=100,default="")
    paragraph = models.TextField(max_length=1000,default="")
    
    def __repr__(self):
        return u"<xlesson id={self.id} " \
            "lesson name={self.lesson_name} " \
            "paragraph={self.paragraph}>".format(self=self)

    class Meta: 
        verbose_name = "xlesson"
        verbose_name_plural = "xlesson"
        ordering = ['course','lesson_name','paragraph']

class Xblockkey(models.Model):
    lesson = models.ForeignKey(Xlesson, on_delete=models.CASCADE)
    keyword = models.TextField(max_length=100,default="")
    defination = models.TextField(max_length=1000,default="")
    
    def __repr__(self):
        return u"<xblockkey id={self.id} " \
            "keyword ={self.keyword} " \
            "defination={self.defination}>".format(self=self)

    class Meta: 
        verbose_name = "xblockkey"
        verbose_name_plural = "xblockkey"
        ordering = ['lesson','keyword','defination']
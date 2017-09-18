"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import json
from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment
from .utils import loader
from workbench.models import Xcourse,Xlesson,Xblockkey
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

class HighXBlock(XBlock):
    
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def studio_view(self, context=None):
        """
        The primary view of the HighXBlock, shown to students
        when viewing courses.
        """
        if context['c_id']:
            course_id=context['c_id']
            lessons=Xlesson.objects.filter(course=course_id)
            course=Xcourse.objects.get(id=course_id)
            context={'lessons':lessons,
                        'scen_id':context['scen_id'],
                        'course':course
                    }
            fragment = Fragment()
            fragment.add_content(loader.render_template('static/html/lessons_list.html', context))
            fragment.add_css(self.resource_string("static/css/lesson_list.css"))
            fragment.add_javascript(self.resource_string("static/js/src/highlight.js"))
            fragment.initialize_js('HighXBlock')
            return fragment

        if context['l_id']:
            lesson_id=context['l_id']
            lesson = Xlesson.objects.filter(id=lesson_id)
            if lesson:
                context={
                    'lesson':lesson[0],
                    'course_id':lesson[0].course_id,
                    'scen_id':context['scen_id']
                }
                fragment = Fragment()
                fragment.add_content(loader.render_template('static/html/paragraph.html', context))
                fragment.add_css(self.resource_string("static/css/paragraph.css"))
                fragment.add_css(self.resource_string("static/css/popup.css"))
                fragment.add_javascript(self.resource_string("static/js/src/highlight.js"))
                fragment.initialize_js('HighXBlock')
                return fragment

        courses=Xcourse.objects.all()
        context = {
                'courses':courses,
                'scen_id': context['scen_id']
            }
        fragment = Fragment()
        fragment.add_content(loader.render_template('static/html/course_list.html', context))
        fragment.add_css(self.resource_string("static/css/highlight.css"))
        fragment.add_javascript(self.resource_string("static/js/src/highlight.js"))
        fragment.initialize_js('HighXBlock')
        return fragment

    def student_view(self, context=None):
        """
        The primary view of the HighXBlock, shown to students
        when viewing courses.
        """
        if context['c_id']:
            course_id=context['c_id']
            lessons=Xlesson.objects.filter(course=course_id)
            course=Xcourse.objects.get(id=course_id)
            context={'lessons':lessons,
                        'scen_id':context['scen_id'],
                        'course':course
                    }
            fragment = Fragment()
            fragment.add_content(loader.render_template('static/html/lessons_list.html', context))
            fragment.add_css(self.resource_string("static/css/lesson_list.css"))
            fragment.add_javascript(self.resource_string("static/js/src/highlight.js"))
            fragment.initialize_js('HighXBlock')
            return fragment

        if context['l_id']:
            lesson_id=context['l_id']
            lesson = Xlesson.objects.filter(id=lesson_id)
            if lesson:
                context={
                    'lesson':lesson[0],
                    'course_id':lesson[0].course_id,
                    'scen_id':context['scen_id']
                }
                fragment = Fragment()
                fragment.add_content(loader.render_template('static/html/paragraph_display.html', context))
                fragment.add_css(self.resource_string("static/css/paragraph.css"))
                fragment.add_css(self.resource_string("static/css/popup.css"))
                fragment.add_css(self.resource_string("static/tooltipster-master/dist/css/tooltipster.bundle.min.css"))
                fragment.add_javascript(self.resource_string("static/tooltipster-master/dist/js/tooltipster.bundle.min.js"))
                fragment.add_javascript(self.resource_string("static/js/src/st_paragraph.js"))
                fragment.initialize_js('StPara')
                return fragment

        courses=Xcourse.objects.all()
        context = {
                'courses':courses,
                'scen_id': context['scen_id']
            }
        fragment = Fragment()
        fragment.add_content(loader.render_template('static/html/course_list.html', context))
        fragment.add_css(self.resource_string("static/css/highlight.css"))
        fragment.add_javascript(self.resource_string("static/js/src/highlight.js"))
        fragment.initialize_js('HighXBlock')
        return fragment


    @XBlock.json_handler
    def save_paragraph(self,data,suffix=''):

        id1=data['lesson_id']
        lesson = Xlesson.objects.filter(id=id1)
        if lesson:
            paragraph=data['paragraph']
            lesson[0].paragraph=paragraph
            lesson[0].save()
            response = {'status':'success',
                        'paragraph':lesson[0].paragraph}
            res=json.dumps(response)
            response=json.loads(res)
            return response            

    @XBlock.json_handler
    def get_keyword(self,data,suffix=''):
        lesson_id=data['lesson_id']
        key=data['key']
        lesson_key = Xblockkey.objects.filter(lesson=lesson_id,keyword=key.lower())
        if lesson_key:
            defination = lesson_key[0].defination
            response = {'status':'success',
                        'key':key,
                        'defination':defination}
            res = json.dumps(response)
            response = json.loads(res)
            return response
        resp={'status':'fail'}
        res = json.dumps(resp)
        resp = json.loads(res)
        return resp 

    @XBlock.json_handler
    def get_initial_keyword(self,data,suffix=''):
        lesson_id=data['lesson_id']
        lesson_key = Xblockkey.objects.filter(lesson=lesson_id)
        if lesson_key:
            list1 ={}
            for i in lesson_key:
                list1[i.keyword]=i.defination

            response = {'status':'success',
                        'list':list1}
            res = json.dumps(response)
            response = json.loads(res)
            return response
        resp={'status':'fail'}
        res = json.dumps(resp)
        resp = json.loads(res)
        return resp                

    @XBlock.json_handler
    def save_keyword(self,data,suffix=''):
        
        lesson_id = data['lesson_id']
        key = data['key']
        defination = data['def']
        lesson = Xlesson.objects.filter(id=lesson_id)
        lesson=lesson[0]
        lesson_key = Xblockkey.objects.filter(lesson=lesson,keyword=key.lower())
        if lesson_key:
            lesson_key =lesson_key[0]
            lesson_key.defination = defination
            lesson_key.save()
        else:
            lesson_key = Xblockkey(lesson=lesson,keyword=key.lower(),defination=defination)   

        lesson_key.save()
        resp = {'status' : 'success',
                'keyword': key}
        response = json.dumps(resp)
        res = json.loads(response)
        return res

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("HighXBlock",
             """<highlight/>
             """),
            ("Multiple HighXBlock",
             """<vertical_demo>
                <highlight/>
                <highlight/>
                <highlight/>
                </vertical_demo>
             """),
        ]

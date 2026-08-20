from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.core.models import Hospital, Department, Specialization
from apps.accounts.models import User, DoctorProfile, PatientProfile
from apps.content.models import Category, Tag, BlogPost
from apps.services.models import ServiceCategory, Service
from apps.patients.models import MedicalHistory, MedicalRecord, PatientDocument, InsuranceInformation


class Command(BaseCommand):
    help = 'Populate database with dummy data for testing Phase 1'

    def handle(self, *args, **options):
        self.stdout.write('Populating dummy data...')
        
        # Create Hospital
        hospital, created = Hospital.objects.get_or_create(
            name='MindCare Medical Center',
            license_number='LIC-MINDCARE-001',
            defaults={
                'address': '123 Healthcare Ave, Medical City',
                'phone': '+1 (555) 123-4567',
                'email': 'info@mindcare.com',
                'website': 'https://mindcare.com',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'Created hospital: {hospital.name}')
        
        # Create Departments
        departments_data = [
            {'name': 'Psychiatry', 'description': 'Mental health and psychiatric services'},
            {'name': 'Psychology', 'description': 'Psychological counseling and therapy'},
            {'name': 'Rehabilitation', 'description': 'Physical and mental rehabilitation programs'},
            {'name': 'Neurology', 'description': 'Neurological disorders and treatment'},
        ]
        
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                hospital=hospital,
                name=dept_data['name'],
                defaults={'description': dept_data['description'], 'is_active': True}
            )
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create Specializations
        specializations_data = [
            {'name': 'Child Psychiatry', 'description': 'Specialized care for children'},
            {'name': 'Adult Psychiatry', 'description': 'Mental health care for adults'},
            {'name': 'Clinical Psychology', 'description': 'Psychological assessment and therapy'},
            {'name': 'Cognitive Behavioral Therapy', 'description': 'CBT specialized treatment'},
            {'name': 'Addiction Recovery', 'description': 'Substance abuse rehabilitation'},
        ]
        
        for spec_data in specializations_data:
            spec, created = Specialization.objects.get_or_create(
                name=spec_data['name'],
                defaults={'description': spec_data['description']}
            )
            if created:
                self.stdout.write(f'Created specialization: {spec.name}')
        
        # Create Content Categories
        categories_data = [
            {'name': 'Mental Health', 'slug': 'mental-health', 'description': 'Articles about mental wellness'},
            {'name': 'Rehabilitation', 'slug': 'rehabilitation', 'description': 'Recovery and rehabilitation tips'},
            {'name': 'Wellness', 'slug': 'wellness', 'description': 'General wellness advice'},
            {'name': 'Child Development', 'slug': 'child-development', 'description': 'Child mental health and development'},
            {'name': 'Senior Care', 'slug': 'senior-care', 'description': 'Elderly mental health and care'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description'], 'is_active': True}
            )
            if created:
                self.stdout.write(f'Created content category: {category.name}')
        
        # Create Tags
        tags_data = ['Depression', 'Anxiety', 'Therapy', 'Wellness', 'Recovery', 'Self-care', 'Autism', 'ADHD', 'PTSD', 'Stress Management']
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
        
        # Create Blog Posts
        category = Category.objects.filter(slug='mental-health').first()
        rehab_category = Category.objects.filter(slug='rehabilitation').first()
        wellness_category = Category.objects.filter(slug='wellness').first()
        tags = list(Tag.objects.all()[:3])
        
        blog_posts_data = [
            {
                'title': 'Understanding Depression: Signs and Symptoms',
                'slug': 'understanding-depression',
                'excerpt': 'Learn about the common signs of depression and when to seek help.',
                'content': 'Depression is a common mental health condition that affects millions of people worldwide. Understanding the signs and symptoms is the first step toward getting help. Common symptoms include persistent sadness, loss of interest in activities, changes in sleep patterns, and difficulty concentrating.',
                'author': self.create_test_user('admin'),
                'category': category,
                'status': 'published'
            },
            {
                'title': '5 Tips for Managing Anxiety',
                'slug': 'managing-anxiety-tips',
                'excerpt': 'Practical strategies to help you cope with anxiety in daily life.',
                'content': 'Anxiety can be overwhelming, but there are effective strategies to manage it. These include deep breathing exercises, regular physical activity, maintaining a healthy diet, getting enough sleep, and seeking support from friends and family.',
                'author': self.create_test_user('admin'),
                'category': category,
                'status': 'published'
            },
            {
                'title': 'The Importance of Mental Health Checkups',
                'slug': 'mental-health-checkups',
                'excerpt': 'Regular mental health screenings are as important as physical checkups.',
                'content': 'Just as we visit doctors for physical checkups, regular mental health checkups are essential for overall well-being. Early detection of mental health issues can lead to better outcomes and more effective treatment options.',
                'author': self.create_test_user('admin'),
                'category': category,
                'status': 'published'
            },
            {
                'title': 'Rehabilitation Recovery Journey',
                'slug': 'rehabilitation-recovery-journey',
                'excerpt': 'Understanding the rehabilitation process and what to expect during recovery.',
                'content': 'Rehabilitation is a journey that requires patience, dedication, and support. Whether recovering from injury, surgery, or addiction, understanding the process helps set realistic expectations and achieve better outcomes.',
                'author': self.create_test_user('admin'),
                'category': rehab_category,
                'status': 'published'
            },
            {
                'title': 'Mindfulness for Daily Wellness',
                'slug': 'mindfulness-daily-wellness',
                'excerpt': 'Incorporate mindfulness practices into your daily routine for better mental health.',
                'content': 'Mindfulness practices can significantly improve mental health and overall well-being. Simple techniques like meditation, deep breathing, and mindful walking can reduce stress and improve focus.',
                'author': self.create_test_user('admin'),
                'category': wellness_category,
                'status': 'published'
            },
            {
                'title': 'Child Mental Health Awareness',
                'slug': 'child-mental-health-awareness',
                'excerpt': 'Recognizing mental health issues in children and early intervention strategies.',
                'content': 'Children can experience mental health challenges just like adults. Early recognition and intervention are crucial for healthy development. Learn about common signs and when to seek professional help.',
                'author': self.create_test_user('admin'),
                'category': Category.objects.filter(slug='child-development').first(),
                'status': 'published'
            },
            {
                'title': 'Senior Mental Health Care',
                'slug': 'senior-mental-health-care',
                'excerpt': 'Addressing the unique mental health needs of elderly populations.',
                'content': 'As we age, mental health needs change. Seniors face unique challenges including loneliness, cognitive decline, and life transitions. Understanding these needs helps provide better care and support.',
                'author': self.create_test_user('admin'),
                'category': Category.objects.filter(slug='senior-care').first(),
                'status': 'published'
            },
        ]
        
        for post_data in blog_posts_data:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title': post_data['title'],
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'author': post_data['author'],
                    'category': post_data['category'],
                    'status': post_data['status'],
                    'published_at': timezone.now()
                }
            )
            if created:
                post.tags.set(tags)
                self.stdout.write(f'Created blog post: {post.title}')
        
        # Create Service Categories
        service_categories_data = [
            {'name': 'Therapy Services', 'slug': 'therapy-services', 'description': 'Individual and group therapy sessions'},
            {'name': 'Rehabilitation Programs', 'slug': 'rehabilitation-programs', 'description': 'Comprehensive rehabilitation services'},
            {'name': 'Assessment Services', 'slug': 'assessment-services', 'description': 'Psychological and psychiatric assessments'},
            {'name': 'Counseling Services', 'slug': 'counseling-services', 'description': 'Professional counseling for various needs'},
            {'name': 'Wellness Programs', 'slug': 'wellness-programs', 'description': 'Holistic wellness and preventive care'},
        ]
        
        for cat_data in service_categories_data:
            service_cat, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description'], 'is_active': True}
            )
            if created:
                self.stdout.write(f'Created service category: {service_cat.name}')
        
        # Create Services
        therapy_cat = ServiceCategory.objects.filter(slug='therapy-services').first()
        rehab_cat = ServiceCategory.objects.filter(slug='rehabilitation-programs').first()
        assessment_cat = ServiceCategory.objects.filter(slug='assessment-services').first()
        
        services_data = [
            {
                'name': 'Individual Therapy Session',
                'slug': 'individual-therapy',
                'short_description': 'One-on-one therapy with licensed professionals',
                'detailed_description': 'Personalized therapy sessions tailored to your specific needs. Our licensed therapists provide evidence-based treatments in a confidential and supportive environment.',
                'category': therapy_cat,
                'price': '150.00',
                'duration_minutes': 60,
                'status': 'active',
                'is_featured': True
            },
            {
                'name': 'Group Therapy Session',
                'slug': 'group-therapy',
                'short_description': 'Supportive group therapy sessions',
                'detailed_description': 'Join others in a supportive group setting to share experiences and learn from one another. Group therapy can be particularly effective for anxiety, depression, and addiction recovery.',
                'category': therapy_cat,
                'price': '75.00',
                'duration_minutes': 90,
                'status': 'active',
                'is_featured': False
            },
            {
                'name': 'Cognitive Behavioral Therapy',
                'slug': 'cognitive-behavioral-therapy',
                'short_description': 'Evidence-based CBT for anxiety and depression',
                'detailed_description': 'Cognitive Behavioral Therapy (CBT) is a proven approach for treating anxiety, depression, and other mental health conditions. Our trained CBT specialists help you identify and change negative thought patterns.',
                'category': therapy_cat,
                'price': '175.00',
                'duration_minutes': 60,
                'status': 'active',
                'is_featured': True
            },
            {
                'name': 'Family Therapy Session',
                'slug': 'family-therapy',
                'short_description': 'Family counseling and relationship therapy',
                'detailed_description': 'Family therapy addresses communication issues, conflicts, and relationship dynamics within families. Our licensed family therapists help families build stronger, healthier relationships.',
                'category': therapy_cat,
                'price': '200.00',
                'duration_minutes': 90,
                'status': 'active',
                'is_featured': False
            },
            {
                'name': 'Addiction Recovery Program',
                'slug': 'addiction-recovery-program',
                'short_description': 'Comprehensive addiction treatment and recovery',
                'detailed_description': 'Our addiction recovery program combines individual therapy, group support, and medical treatment to help individuals overcome substance abuse. We provide personalized treatment plans for lasting recovery.',
                'category': rehab_cat,
                'price': '250.00',
                'duration_minutes': 120,
                'status': 'active',
                'is_featured': True
            },
            {
                'name': 'Physical Rehabilitation',
                'slug': 'physical-rehabilitation',
                'short_description': 'Physical therapy and rehabilitation services',
                'detailed_description': 'Comprehensive physical rehabilitation for injury recovery, post-surgical care, and mobility improvement. Our licensed physical therapists create personalized treatment plans.',
                'category': rehab_cat,
                'price': '125.00',
                'duration_minutes': 60,
                'status': 'active',
                'is_featured': False
            },
            {
                'name': 'Psychological Assessment',
                'slug': 'psychological-assessment',
                'short_description': 'Comprehensive psychological evaluation and testing',
                'detailed_description': 'Our psychological assessments provide comprehensive evaluation of mental health conditions, cognitive functioning, and emotional well-being. Results guide personalized treatment planning.',
                'category': assessment_cat,
                'price': '300.00',
                'duration_minutes': 90,
                'status': 'active',
                'is_featured': True
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')
        
        # Create Test Users
        patient_user = self.create_test_user('patient', role='patient')
        doctor_user = self.create_test_user('doctor', role='doctor')
        
        # Phase 2: Patient Management System Dummy Data
        self.create_patient_dummy_data(patient_user, doctor_user)
        
        self.stdout.write(self.style.SUCCESS('Dummy data populated successfully!'))
    
    def create_test_user(self, username, role='patient'):
        """Create a test user with the specified role"""
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=f'{username}@mindcare.com',
                password='Test123456',
                first_name=username.capitalize(),
                last_name='User',
                role=role,
                privacy_consent_accepted=True,
                data_processing_consent=True,
                terms_accepted=True
            )
            
            if role == 'doctor':
                # Create doctor profile
                specialization = Specialization.objects.first()
                department = Department.objects.first()
                hospital = Hospital.objects.first()
                
                doctor_profile = DoctorProfile.objects.create(
                    user=user,
                    license_number=f'LIC{username.upper()}12345',
                    qualification='MD, Psychiatry',
                    experience_years=5,
                    consultation_fee=150.00
                )
                doctor_profile.specialization.set([specialization])
            elif role == 'patient':
                # Create patient profile
                PatientProfile.objects.create(
                    user=user,
                    blood_group='O+',
                    allergies='None',
                    chronic_conditions='None',
                    current_medications='None'
                )
            
            self.stdout.write(f'Created test user: {username} ({role})')
            return user
    
    def create_patient_dummy_data(self, patient_user, doctor_user):
        """Create Phase 2 patient management system dummy data"""
        self.stdout.write('Creating Phase 2 patient dummy data...')
        
        # Create Medical History entries (5 entries)
        medical_histories_data = [
            {
                'condition_name': 'Generalized Anxiety Disorder',
                'diagnosis_date': datetime(2023, 6, 15).date(),
                'therapy_history': 'Started CBT therapy in June 2023. Showed significant improvement after 8 sessions.',
                'current_medications': 'Sertraline 50mg daily',
                'notes': 'Patient responds well to therapy. Continue current treatment plan.',
                'status': 'in_treatment'
            },
            {
                'condition_name': 'Major Depressive Disorder',
                'diagnosis_date': datetime(2022, 11, 20).date(),
                'therapy_history': 'Initial diagnosis in November 2022. Completed 12-week intensive therapy program.',
                'current_medications': 'Fluoxetine 20mg daily',
                'notes': 'Currently in remission. Maintain monthly check-ins.',
                'status': 'in_remission'
            },
            {
                'condition_name': 'PTSD (Post-Traumatic Stress Disorder)',
                'diagnosis_date': datetime(2023, 2, 10).date(),
                'therapy_history': 'Trauma-focused therapy initiated. EMDR sessions showing positive results.',
                'current_medications': 'Prazosin 2mg at bedtime',
                'notes': 'Nightmares reduced by 60%. Continue EMDR therapy.',
                'status': 'active'
            },
            {
                'condition_name': 'Panic Disorder with Agoraphobia',
                'diagnosis_date': datetime(2023, 8, 5).date(),
                'therapy_history': 'Exposure therapy started. Gradual improvement in social situations.',
                'current_medications': 'Alprazolam 0.5mg as needed',
                'notes': 'Patient making steady progress. Reduce frequency of panic attacks.',
                'status': 'in_treatment'
            },
            {
                'condition_name': 'Social Anxiety Disorder',
                'diagnosis_date': datetime(2023, 4, 18).date(),
                'therapy_history': 'Group therapy and individual CBT. Improved confidence in social settings.',
                'current_medications': 'Propranolol 20mg before social events',
                'notes': 'Significant improvement. Continue current treatment plan.',
                'status': 'in_remission'
            },
        ]
        
        for history_data in medical_histories_data:
            history, created = MedicalHistory.objects.get_or_create(
                patient=patient_user,
                condition_name=history_data['condition_name'],
                defaults=history_data
            )
            if created:
                self.stdout.write(f'Created medical history: {history.condition_name}')
        
        # Create Medical Records (5 entries)
        medical_records_data = [
            {
                'doctor_name': f'Dr. {doctor_user.first_name} {doctor_user.last_name}',
                'visit_date': timezone.make_aware(datetime(2024, 1, 15, 10, 30)),
                'mental_health_diagnosis': 'Generalized Anxiety Disorder - follow-up',
                'therapy_notes': 'Patient reports 70% reduction in anxiety symptoms. CBT techniques working well. Sleep quality improved.',
                'prescription_details': 'Continue Sertraline 50mg daily. Add relaxation exercises.',
                'recommended_treatment_plan': 'Continue weekly CBT sessions for 4 more weeks, then bi-weekly.'
            },
            {
                'doctor_name': f'Dr. {doctor_user.first_name} {doctor_user.last_name}',
                'visit_date': timezone.make_aware(datetime(2024, 2, 20, 14, 0)),
                'mental_health_diagnosis': 'Major Depressive Disorder - maintenance',
                'therapy_notes': 'Patient maintaining remission. No depressive symptoms reported. Good medication compliance.',
                'prescription_details': 'Continue Fluoxetine 20mg daily.',
                'recommended_treatment_plan': 'Monthly maintenance appointments. Continue current medication.'
            },
            {
                'doctor_name': f'Dr. {doctor_user.first_name} {doctor_user.last_name}',
                'visit_date': timezone.make_aware(datetime(2024, 3, 10, 9, 0)),
                'mental_health_diagnosis': 'PTSD - EMDR session 8',
                'therapy_notes': 'Completed 8th EMDR session. Patient reports significant reduction in flashbacks and nightmares.',
                'prescription_details': 'Continue Prazosin 2mg at bedtime.',
                'recommended_treatment_plan': 'Continue EMDR therapy. Consider tapering off medication in 2 months.'
            },
            {
                'doctor_name': f'Dr. {doctor_user.first_name} {doctor_user.last_name}',
                'visit_date': timezone.make_aware(datetime(2024, 4, 5, 11, 30)),
                'mental_health_diagnosis': 'Panic Disorder - progress review',
                'therapy_notes': 'Patient successfully attended 3 social events this month. Panic attacks reduced from weekly to monthly.',
                'prescription_details': 'Alprazolam 0.5mg as needed (currently using 1-2 times per month).',
                'recommended_treatment_plan': 'Continue exposure therapy. Gradually reduce medication dependency.'
            },
            {
                'doctor_name': f'Dr. {doctor_user.first_name} {doctor_user.last_name}',
                'visit_date': timezone.make_aware(datetime(2024, 5, 15, 15, 0)),
                'mental_health_diagnosis': 'Social Anxiety Disorder - group therapy',
                'therapy_notes': 'Patient participated in group therapy session. Reported feeling comfortable sharing with peers.',
                'prescription_details': 'Propranolol 20mg before social events (rarely needed now).',
                'recommended_treatment_plan': 'Continue group therapy. Consider transitioning to monthly check-ins.'
            },
        ]
        
        for record_data in medical_records_data:
            record, created = MedicalRecord.objects.get_or_create(
                patient=patient_user,
                visit_date=record_data['visit_date'],
                defaults=record_data
            )
            if created:
                self.stdout.write(f'Created medical record: {record.visit_date.strftime("%Y-%m-%d")}')
        
        # Create Patient Documents (5 entries)
        # Note: We'll create these without actual files for testing
        patient_documents_data = [
            {
                'document_title': 'Psychological Assessment - Initial Evaluation',
                'document_type': 'psychological_assessment',
                'notes': 'Comprehensive psychological evaluation conducted on June 15, 2023.',
                'uploaded_at': datetime(2023, 6, 15, 14, 30)
            },
            {
                'document_title': 'PHQ-9 Depression Scale Results',
                'document_type': 'self_report_scale',
                'notes': 'PHQ-9 score: 12 (Moderate depression). Baseline measurement.',
                'uploaded_at': datetime(2023, 11, 25, 10, 0)
            },
            {
                'document_title': 'GAD-7 Anxiety Scale Results',
                'document_type': 'self_report_scale',
                'notes': 'GAD-7 score: 14 (Moderate anxiety). Pre-treatment baseline.',
                'uploaded_at': datetime(2023, 6, 20, 11, 15)
            },
            {
                'document_title': 'CBT Therapy Notes - Session 1-4',
                'document_type': 'therapy_notes',
                'notes': 'Summary of initial CBT sessions focusing on cognitive restructuring.',
                'uploaded_at': datetime(2023, 7, 15, 16, 0)
            },
            {
                'document_title': 'Insurance Authorization for Therapy',
                'document_type': 'insurance_document',
                'notes': 'Pre-authorization for 12 CBT sessions approved by insurance.',
                'uploaded_at': datetime(2023, 6, 10, 9, 30)
            },
        ]
        
        for doc_data in patient_documents_data:
            doc, created = PatientDocument.objects.get_or_create(
                patient=patient_user,
                document_title=doc_data['document_title'],
                defaults={
                    **doc_data,
                    'file': None  # No actual file for testing
                }
            )
            if created:
                self.stdout.write(f'Created patient document: {doc.document_title}')
        
        # Create Insurance Information (1 entry - OneToOneField)
        insurance_info, created = InsuranceInformation.objects.get_or_create(
            patient=patient_user,
            defaults={
                'provider_name': 'Blue Cross Blue Shield',
                'policy_number': 'POL-PATIENT001',
                'mental_health_coverage_details': 'Covers 20 therapy sessions per calendar year. $50 copay per session. Prior authorization required for more than 8 sessions.',
                'copay_amount': 50.00,
                'expiry_date': datetime(2025, 12, 31).date(),
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'Created insurance information: {insurance_info.provider_name}')

from django.test import TestCase
from catalog.models import GPPractices, GPPractitioners, GPDetails, GPPopulations


class DashboardFrontendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.practice = GPPractices.objects.create(
            practice_code="20002",
            name="Riverbank Health Centre",
            list_size=3200,
            address="45 Riverside Road",
            postcode="AB10 1AA",
            telephone="01382555123",
            health_board="NHS Grampian",
            latitude=57.1497,
            longitude=-2.0943,
        )

        cls.doctor = GPPractitioners.objects.create(
            medical_council_number="GMC002",
            forename="James",
            surname="MacLeod",
            sex="Male",
        )

        GPDetails.objects.create(
            gp_code=cls.doctor,
            practice=cls.practice,
            designation="Salaried GP",
        )

        GPPopulations.objects.create(
            practice=cls.practice,
            sex="Female",
            ages00to04=150,
            ages05to09=180,
            ages10to14=170,
            ages15to19=160,
            ages20to24=210,
            ages25to29=220,
            ages30to34=230,
            ages35to39=240,
            ages40to44=250,
            ages45to49=260,
            ages50to54=270,
            ages55to59=280,
            ages60to64=290,
            ages65to69=300,
            ages70to74=310,
            ages75to79=320,
            ages80to84=330,
            ages85plus=340,
        )

        GPPopulations.objects.create(
            practice=cls.practice,
            sex="Male",
            ages00to04=140,
            ages05to09=175,
            ages10to14=165,
            ages15to19=155,
            ages20to24=205,
            ages25to29=215,
            ages30to34=225,
            ages35to39=235,
            ages40to44=245,
            ages45to49=255,
            ages50to54=265,
            ages55to59=275,
            ages60to64=285,
            ages65to69=295,
            ages70to74=305,
            ages75to79=315,
            ages80to84=325,
            ages85plus=335,
        )

    def test_dashboard_page_loads(self):
        response = self.client.get("/tables/practices")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table/dashboard.html")
        self.assertContains(response, "GP Practice Dashboard")
        self.assertContains(response, "Riverbank Health Centre")

    def test_home_redirects_to_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/tables/practices")

    def test_postcode_search_filters_results(self):
        response = self.client.get("/tables/practices", {"postcode": "AB10"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riverbank Health Centre")
        self.assertContains(response, "AB10 1AA")

    def test_patient_size_filter_loads(self):
        response = self.client.get(
            "/tables/practices/filters",
            {"patient_size": "2501-5000", "pagesize": "5"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table/dashboard.html")
        self.assertContains(response, "Riverbank Health Centre")

    def test_practice_detail_page_loads(self):
        response = self.client.get("/practices/20002/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/practice_detail.html")
        self.assertContains(response, "Riverbank Health Centre")
        self.assertContains(response, "GP Doctors")
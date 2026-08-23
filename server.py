from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import Optional, List

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

IMG = "auto=format&fit=crop&w=940&q=80"
U = "https://images.unsplash.com"

DEVICES = [
    {
        "id": "mri-15t", "category": "imaging", "department": "radiology", "price": 1200000,
        "name_en": "MRI Scanner 1.5T", "name_ar": "جهاز الرنين المغناطيسي 1.5 تسلا",
        "tagline_en": "Superconducting magnetic resonance imaging", "tagline_ar": "تصوير بالرنين المغناطيسي فائق التوصيل",
        "image": "https://images.pexels.com/photos/13176356/pexels-photo-13176356.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "description_en": "A superconducting MRI system delivering high-resolution soft-tissue imaging for neurology, orthopedics and oncology. Wide-bore design improves patient comfort while advanced coils cut scan times significantly.",
        "description_ar": "نظام رنين مغناطيسي فائق التوصيل يوفّر صوراً عالية الدقة للأنسجة الرخوة في طب الأعصاب والعظام والأورام. تصميم النفق الواسع يحسّن راحة المريض بينما تختصر الملفات المتقدمة زمن الفحص بشكل كبير.",
        "principle_en": "A powerful 1.5-tesla magnet aligns hydrogen protons in the body. Radiofrequency pulses knock them out of alignment, and as they realign they emit signals that gradient coils localize in space; a computer reconstructs these signals into detailed cross-sectional images without ionizing radiation.",
        "principle_ar": "يقوم مغناطيس بقوة 1.5 تسلا بمحاذاة بروتونات الهيدروجين في الجسم، ثم تخرجها النبضات الراديوية عن محاذاتها، وعند عودتها تصدر إشارات تحددها ملفات التدرج في الفضاء، ليعيد الحاسوب بناء هذه الإشارات إلى صور مقطعية دقيقة دون أي إشعاع مؤين.",
        "components": [
            {"en": "Superconducting magnet (1.5T)", "ar": "مغناطيس فائق التوصيل (1.5 تسلا)"},
            {"en": "Gradient coil system", "ar": "منظومة ملفات التدرج"},
            {"en": "RF transmitter & receiver coils", "ar": "ملفات الإرسال والاستقبال الراديوية"},
            {"en": "Cryogenic cooling (helium) system", "ar": "نظام التبريد بالهيليوم"},
            {"en": "Patient table & positioning unit", "ar": "طاولة المريض ووحدة التموضع"},
            {"en": "Reconstruction computer & console", "ar": "حاسوب إعادة البناء ووحدة التحكم"},
        ],
        "specs": [
            {"label_en": "Field strength", "label_ar": "شدة المجال", "value": "1.5 Tesla"},
            {"label_en": "Bore diameter", "label_ar": "قطر النفق", "value": "70 cm"},
            {"label_en": "Gradient strength", "label_ar": "قوة التدرج", "value": "45 mT/m"},
            {"label_en": "Weight", "label_ar": "الوزن", "value": "5,600 kg"},
        ],
    },
    {
        "id": "ct-128", "category": "imaging", "department": "radiology", "price": 850000,
        "name_en": "CT Scanner 128-Slice", "name_ar": "جهاز الأشعة المقطعية 128 مقطعاً",
        "tagline_en": "High-speed computed tomography", "tagline_ar": "تصوير مقطعي محوسب فائق السرعة",
        "image": f"{U}/photo-1550831107-1553da8c8464?{IMG}",
        "description_en": "A 128-slice CT scanner built for emergency, cardiac and whole-body imaging. Sub-second rotation and iterative dose reduction deliver sharp images at a fraction of traditional radiation doses.",
        "description_ar": "جهاز أشعة مقطعية بـ128 مقطعاً مصمم للطوارئ وتصوير القلب والجسم الكامل. سرعة دوران أقل من ثانية وتقنية تقليل الجرعة التكرارية تمنحان صوراً حادة بجزء يسير من الإشعاع التقليدي.",
        "principle_en": "An X-ray tube rotates around the patient while a detector ring captures attenuation data from thousands of angles per second. A computer applies filtered back-projection and iterative reconstruction to build cross-sectional slices of the body.",
        "principle_ar": "يدور أنبوب الأشعة السينية حول المريض بينما يلتقط حلقة الكواشف بيانات التوهين من آلاف الزوايا في الثانية، ثم يطبق الحاسوب الإسقاط الخلفي المرشح وإعادة البناء التكرارية لتكوين مقاطع عرضية للجسم.",
        "components": [
            {"en": "Rotating gantry with X-ray tube", "ar": "الإطار الدوّار مع أنبوب الأشعة"},
            {"en": "Solid-state detector ring", "ar": "حلقة الكواشف الصلبة"},
            {"en": "High-voltage generator (120 kW)", "ar": "مولد الجهد العالي (120 كيلوواط)"},
            {"en": "Motorized patient couch", "ar": "سرير المريض الآلي"},
            {"en": "Reconstruction & dose-modulation computer", "ar": "حاسوب إعادة البناء وضبط الجرعة"},
            {"en": "Operator console & injectors", "ar": "وحدة تحكم المشغل ومضخات الصبغة"},
        ],
        "specs": [
            {"label_en": "Slices", "label_ar": "عدد المقاطع", "value": "128"},
            {"label_en": "Rotation time", "label_ar": "زمن الدورة", "value": "0.35 s"},
            {"label_en": "Generator", "label_ar": "المولد", "value": "120 kW"},
            {"label_en": "Max table load", "label_ar": "أقصى حمولة", "value": "227 kg"},
        ],
    },
    {
        "id": "us-4d", "category": "imaging", "department": "clinic", "price": 45000,
        "name_en": "4D Ultrasound System", "name_ar": "جهاز الموجات فوق الصوتية رباعي الأبعاد",
        "tagline_en": "Real-time volumetric sonography", "tagline_ar": "تصوير حجمي فوري بالموجات الصوتية",
        "image": f"{U}/photo-1583911860205-72f8ac8ddcbe?{IMG}",
        "description_en": "A cart-based 4D ultrasound platform for obstetrics, cardiology and general imaging. Crystal-clear probe technology with elastography and Doppler modes in a compact, clinic-ready form.",
        "description_ar": "منصة موجات فوق صوتية رباعية الأبعاد على عربة لطب النساء والقلب والتصوير العام. تقنية مجسات فائقة النقاء مع أنماط الإيلاستوغرافي والدوبلر في تصميم مدمج مناسب للعيادات.",
        "principle_en": "A piezoelectric transducer emits high-frequency sound waves (2–18 MHz) into the body. Echoes reflected from tissue boundaries return to the probe, and the system converts their timing and intensity into live 2D, 3D and moving 4D images — completely radiation-free.",
        "principle_ar": "يرسل مجس كهرضغطي موجات صوتية عالية التردد (2–18 ميغاهرتز) إلى الجسم، فترتد الأصداء من حدود الأنسجة عائدة إلى المجس، ويحوّل النظام توقيتها وشدتها إلى صور حية ثنائية وثلاثية الأبعاد ورباعية متحركة — دون أي إشعاع.",
        "components": [
            {"en": "Convex, linear & volumetric probes", "ar": "مجسات محدبة وخطية وحجمية"},
            {"en": "Piezoelectric beamformer", "ar": "مشكّل الحزم الكهرضغطي"},
            {"en": "21.5\" HD imaging monitor", "ar": "شاشة تصوير عالية الدقة 21.5 بوصة"},
            {"en": "Doppler & elastography modules", "ar": "وحدتا الدوبلر والإيلاستوغرافي"},
            {"en": "Height-adjustable cart", "ar": "عربة قابلة لتعديل الارتفاع"},
            {"en": "Image archive (DICOM) software", "ar": "برنامج الأرشفة (DICOM)"},
        ],
        "specs": [
            {"label_en": "Frequency range", "label_ar": "نطاق التردد", "value": "2–18 MHz"},
            {"label_en": "Probe ports", "label_ar": "منافذ المجسات", "value": "4"},
            {"label_en": "Modes", "label_ar": "الأنماط", "value": "B / M / Color / 4D"},
            {"label_en": "Boot time", "label_ar": "زمن التشغيل", "value": "25 s"},
        ],
    },
    {
        "id": "xray-dr", "category": "imaging", "department": "radiology", "price": 120000,
        "name_en": "Digital X-Ray (DR)", "name_ar": "جهاز الأشعة السينية الرقمي",
        "tagline_en": "Direct digital radiography suite", "tagline_ar": "جناح أشعة رقمية مباشرة",
        "image": f"{U}/photo-1581595219315-a187dd40c322?{IMG}",
        "description_en": "A floor-mounted digital radiography room with wireless flat-panel detectors. Instant image preview, automatic stitching and low-dose pediatric protocols for high-throughput departments.",
        "description_ar": "غرفة أشعة رقمية مثبتة أرضياً مع كواشف لوحية لاسلكية. معاينة فورية للصور ولصق آلي وبروتوكولات جرعات منخفضة للأطفال تناسب الأقسام عالية الضغط.",
        "principle_en": "X-rays generated in the tube pass through the patient and strike a flat-panel detector, where a scintillator converts them to light and photodiodes convert light to charge. The digital image appears on the workstation within seconds — no film, no cassettes.",
        "principle_ar": "تخترق الأشعة السينية المتولدة في الأنبوب جسم المريض وتصطدم بكاشف لوحي، حيث يحوّلها الوميضي إلى ضوء ثم تحوّله الثنائيات الضوئية إلى شحنة كهربائية، لتظهر الصورة الرقمية على محطة العمل خلال ثوانٍ — دون أفلام أو كاسيتات.",
        "components": [
            {"en": "Ceiling/floor tube stand", "ar": "حامل الأنبوب الأرضي/السقفي"},
            {"en": "Wireless flat-panel detectors (2×)", "ar": "كاشفان لوحيان لاسلكيان"},
            {"en": "80 kW high-frequency generator", "ar": "مولد عالي التردد 80 كيلوواط"},
            {"en": "Vertical wall stand (Bucky)", "ar": "الحامل الجداري العمودي"},
            {"en": "Floating patient table", "ar": "طاولة المريض العائمة"},
            {"en": "Acquisition workstation & PACS link", "ar": "محطة الالتقاط وربط PACS"},
        ],
        "specs": [
            {"label_en": "Detector size", "label_ar": "حجم الكاشف", "value": "43×43 cm"},
            {"label_en": "Pixel pitch", "label_ar": "بُعد البكسل", "value": "139 µm"},
            {"label_en": "kV range", "label_ar": "نطاق الجهد", "value": "40–150 kV"},
            {"label_en": "Preview time", "label_ar": "زمن المعاينة", "value": "< 3 s"},
        ],
    },
    {
        "id": "ecg-12", "category": "diagnostics", "department": "cardiology", "price": 3500,
        "name_en": "12-Lead ECG Machine", "name_ar": "جهاز تخطيط القلب 12 قناة",
        "tagline_en": "Resting electrocardiography with interpretation", "tagline_ar": "تخطيط قلب مع تحليل آلي",
        "image": f"{U}/photo-1530026405186-ed1f139313f8?{IMG}",
        "description_en": "A portable 12-lead ECG with automated interpretation algorithms and on-screen waveform review. One-touch acquisition, internal memory for 1,000 exams and direct EMR export.",
        "description_ar": "جهاز تخطيط قلب محمول بـ12 قناة مع خوارزميات تفسير آلي ومراجعة الموجات على الشاشة. التقاط بلمسة واحدة وذاكرة داخلية لألف فحص وتصدير مباشر للسجلات الطبية.",
        "principle_en": "Electrodes on the limbs and chest pick up the heart's tiny electrical potentials (millivolts). Amplifiers and filters clean the signal, and the machine plots 12 simultaneous views of cardiac electrical activity to reveal arrhythmias, ischemia and hypertrophy.",
        "principle_ar": "تلتقط أقطاب كهربائية على الأطراف والصدر الجهود الكهربائية الدقيقة للقلب (بالملي فولت)، ثم تنظف المكبرات والمرشحات الإشارة، ويرسم الجهاز 12 منظراً متزامناً للنشاط الكهربائي القلبي لكشف اضطرابات النظم ونقص التروية والتضخم.",
        "components": [
            {"en": "10-lead patient cable set", "ar": "طقم كابلات المريض (10 أقطاب)"},
            {"en": "Bio-potential amplifier stage", "ar": "مرحلة تضخيم الجهد الحيوي"},
            {"en": "8\" color touchscreen", "ar": "شاشة لمس ملونة 8 بوصات"},
            {"en": "Thermal printer (210 mm)", "ar": "طابعة حرارية 210 ملم"},
            {"en": "Interpretation software module", "ar": "وحدة برمجيات التفسير"},
            {"en": "Rechargeable Li-ion battery", "ar": "بطارية ليثيوم قابلة للشحن"},
        ],
        "specs": [
            {"label_en": "Channels", "label_ar": "القنوات", "value": "12"},
            {"label_en": "Sampling", "label_ar": "معدل العينات", "value": "16,000 Hz"},
            {"label_en": "Memory", "label_ar": "الذاكرة", "value": "1,000 exams"},
            {"label_en": "Battery", "label_ar": "البطارية", "value": "6 h"},
        ],
    },
    {
        "id": "monitor-pm", "category": "monitoring", "department": "icu", "price": 4800,
        "name_en": "Multiparameter Patient Monitor", "name_ar": "جهاز مراقبة العلامات الحيوية",
        "tagline_en": "Continuous vital-signs surveillance", "tagline_ar": "مراقبة مستمرة للعلامات الحيوية",
        "image": f"{U}/photo-1631815589968-fdb09a223b1e?{IMG}",
        "description_en": "A bedside monitor tracking ECG, SpO2, NIBP, respiration and dual temperature with optional EtCO2 and invasive pressures. Network-ready with central-station integration for ICU and ER.",
        "description_ar": "جهاز مراقبة بجانب السرير يتتبع تخطيط القلب وتشبع الأكسجين وضغط الدم غير الباضع والتنفس ودرجة الحرارة المزدوجة مع خيارات ثاني أكسيد الكربون والضغوط الباضعة. جاهز للشبكة والتكامل مع المحطة المركزية للعناية والطوارئ.",
        "principle_en": "Sensors convert physiology into electrical signals: ECG electrodes read cardiac potentials, a SpO2 probe measures light absorption of oxygenated blood, and an oscillometric cuff derives blood pressure. The unit trends all parameters and alarms on preset limits.",
        "principle_ar": "تحوّل المستشعرات وظائف الجسم إلى إشارات كهربائية: أقطاب القلب تقرأ الجهود القلبية، ومجس الأكسجين يقيس امتصاص الدم المؤكسج للضوء، ورباط الضغط التذبذبي يستنتج ضغط الدم. يعرض الجهاز اتجاهات كل المعايير وينذر عند تجاوز الحدود.",
        "components": [
            {"en": "15\" capacitive display unit", "ar": "وحدة عرض لمسية 15 بوصة"},
            {"en": "ECG/RESP module & cables", "ar": "وحدة تخطيط القلب/التنفس وكابلاتها"},
            {"en": "SpO2 sensor & module", "ar": "مجس ووحدة تشبع الأكسجين"},
            {"en": "NIBP pump, valve & cuffs", "ar": "مضخة وصمام وأربطة ضغط الدم"},
            {"en": "EtCO2 / IBP expansion slots", "ar": "منافذ توسعة ثاني أكسيد الكربون/الضغط الباضع"},
            {"en": "Central-station network card", "ar": "بطاقة شبكة المحطة المركزية"},
        ],
        "specs": [
            {"label_en": "Parameters", "label_ar": "المعايير", "value": "6+"},
            {"label_en": "Display", "label_ar": "الشاشة", "value": "15\" touch"},
            {"label_en": "Trend memory", "label_ar": "ذاكرة الاتجاهات", "value": "240 h"},
            {"label_en": "Battery", "label_ar": "البطارية", "value": "4 h"},
        ],
    },
    {
        "id": "vent-icu", "category": "life_support", "department": "icu", "price": 28000,
        "name_en": "ICU Ventilator", "name_ar": "جهاز التنفس الصناعي للعناية المركزة",
        "tagline_en": "Invasive & non-invasive ventilation", "tagline_ar": "تهوية باضعة وغير باضعة",
        "image": f"{U}/photo-1584982751601-97dcc096659c?{IMG}",
        "description_en": "A turbine-based ICU ventilator supporting neonatal to adult patients. Advanced modes including PRVC, APRV and NIV with integrated capnography and SpO2 feedback for lung-protective ventilation.",
        "description_ar": "جهاز تنفس صناعي توربيني للعناية المركزة يدعم المرضى من حديثي الولادة إلى البالغين. أنماط متقدمة تشمل PRVC وAPRV والتهوية غير الباضعة مع قياس ثاني أكسيد الكربون وتغذية راجعة للأكسجين لحماية الرئتين.",
        "principle_en": "A high-speed turbine generates controlled airflow. Microprocessors adjust pressure, volume and oxygen concentration breath-by-breath using closed-loop feedback from flow and pressure sensors, synchronizing with — or fully replacing — the patient's breathing effort.",
        "principle_ar": "تولّد توربينة عالية السرعة تدفق هواء مضبوطاً، وتضبط المعالجات الدقيقة الضغط والحجم وتركيز الأكسجين نفساً بنفس عبر تغذية راجعة مغلقة من مستشعرات التدفق والضغط، متزامنة مع جهد تنفس المريض أو مستبدلة له بالكامل.",
        "components": [
            {"en": "Turbine gas-delivery unit", "ar": "وحدة توصيل الغاز التوربينية"},
            {"en": "Inspiratory/expiratory valves", "ar": "صمامات الشهيق والزفير"},
            {"en": "Flow, pressure & O2 sensors", "ar": "مستشعرات التدفق والضغط والأكسجين"},
            {"en": "Heated humidifier chamber", "ar": "غرفة الترطيب المسخّنة"},
            {"en": "Patient breathing circuits", "ar": "دوائر تنفس المريض"},
            {"en": "15\" touch control screen", "ar": "شاشة تحكم لمسية 15 بوصة"},
        ],
        "specs": [
            {"label_en": "Modes", "label_ar": "الأنماط", "value": "12+"},
            {"label_en": "Tidal volume", "label_ar": "الحجم الجاري", "value": "2–2500 mL"},
            {"label_en": "FiO2", "label_ar": "تركيز الأكسجين", "value": "21–100%"},
            {"label_en": "Internal battery", "label_ar": "البطارية الداخلية", "value": "3 h"},
        ],
    },
    {
        "id": "aed-defib", "category": "life_support", "department": "emergency", "price": 2200,
        "name_en": "AED Defibrillator", "name_ar": "جهاز الصدمات الكهربائية (مزيل الرجفان)",
        "tagline_en": "Automated external defibrillation", "tagline_ar": "إزالة رجفان خارجية آلية",
        "image": f"{U}/photo-1624727828489-a1e03b79bba8?{IMG}",
        "description_en": "A rugged automated external defibrillator with voice-and-visual coaching for lay rescuers. Biphasic waveform, CPR feedback and self-testing ensure readiness in public spaces and ambulances.",
        "description_ar": "جهاز إزالة رجفان خارجي آلي متين مع إرشاد صوتي ومرئي للمسعفين غير المتخصصين. موجة ثنائية الطور وتغذية راجعة للإنعاش القلبي وفحص ذاتي لضمان الجاهزية في الأماكن العامة وسيارات الإسعاف.",
        "principle_en": "Adhesive pads analyze the heart's rhythm; if ventricular fibrillation or pulseless tachycardia is detected, a capacitor charges and delivers a controlled biphasic shock (120–200 J) through the chest to reset the heart's electrical activity.",
        "principle_ar": "تحلل اللصقات نظم القلب، وعند كشف الرجفان البطيني أو تسرع القلب بلا نبض، يُشحن مكثف كهربائي ويطلق صدمة ثنائية الطور مضبوطة (120–200 جول) عبر الصدر لإعادة ضبط النشاط الكهربائي للقلب.",
        "components": [
            {"en": "Biphasic defibrillation module", "ar": "وحدة الصدمات ثنائية الطور"},
            {"en": "High-voltage capacitor bank", "ar": "مجموعة المكثفات عالية الجهد"},
            {"en": "Pre-connected electrode pads", "ar": "لصقات أقطاب موصولة مسبقاً"},
            {"en": "Rhythm-analysis processor", "ar": "معالج تحليل النظم"},
            {"en": "Voice prompt speaker system", "ar": "نظام الإرشاد الصوتي"},
            {"en": "Long-life standby battery", "ar": "بطارية استعداد طويلة العمر"},
        ],
        "specs": [
            {"label_en": "Energy", "label_ar": "الطاقة", "value": "120–200 J"},
            {"label_en": "Charge time", "label_ar": "زمن الشحن", "value": "< 8 s"},
            {"label_en": "Ingress rating", "label_ar": "مقاومة العوامل", "value": "IP55"},
            {"label_en": "Weight", "label_ar": "الوزن", "value": "2.4 kg"},
        ],
    },
    {
        "id": "infusion-pump", "category": "monitoring", "department": "ward", "price": 1500,
        "name_en": "Volumetric Infusion Pump", "name_ar": "مضخة المحاليل الوريدية",
        "tagline_en": "Precision IV fluid delivery", "tagline_ar": "ضخ وريدي دقيق للسوائل",
        "image": f"{U}/photo-1631815588090-d4bfec5b1ccb?{IMG}",
        "description_en": "A stackable volumetric pump delivering fluids, nutrients and medication at ±2% accuracy. Drug library with dose-error reduction, anti-bolus safety and wireless ward networking.",
        "description_ar": "مضخة حجمية قابلة للتكديس توصل السوائل والمغذيات والأدوية بدقة ±2%. مكتبة أدوية مع تقليل أخطاء الجرعات وحماية من الدفقات المفاجئة وربط لاسلكي بشبكة الجناح.",
        "principle_en": "A peristaltic finger mechanism compresses the IV tubing in sequence, propelling precisely measured volumes. Ultrasonic air sensors, occlusion pressure detection and software dose-limits guarantee safe, uninterrupted delivery from 0.1 to 1,200 mL/h.",
        "principle_ar": "تضغط آلية تمعجية الأنبوب الوريدي بالتتابع فتدفع أحجاماً مقيسة بدقة، بينما تضمن مستشعرات الهواء فوق الصوتية وكشف ضغط الانسداد وحدود الجرعات البرمجية ضخاً آمناً متواصلاً من 0.1 إلى 1200 مل/ساعة.",
        "components": [
            {"en": "Peristaltic pumping mechanism", "ar": "الآلية التمعجية للضخ"},
            {"en": "Ultrasonic air-in-line sensor", "ar": "مستشعر الهواء فوق الصوتي"},
            {"en": "Occlusion pressure sensor", "ar": "مستشعر ضغط الانسداد"},
            {"en": "Drug-library control software", "ar": "برمجية التحكم بمكتبة الأدوية"},
            {"en": "Pole clamp & stacking frame", "ar": "مشبك العمود وإطار التكديس"},
            {"en": "Backup battery (8 h)", "ar": "بطارية احتياطية (8 ساعات)"},
        ],
        "specs": [
            {"label_en": "Flow range", "label_ar": "نطاق التدفق", "value": "0.1–1200 mL/h"},
            {"label_en": "Accuracy", "label_ar": "الدقة", "value": "±2%"},
            {"label_en": "Drug library", "label_ar": "مكتبة الأدوية", "value": "5,000 entries"},
            {"label_en": "Weight", "label_ar": "الوزن", "value": "1.8 kg"},
        ],
    },
    {
        "id": "anesthesia-ws", "category": "surgical", "department": "operating_room", "price": 65000,
        "name_en": "Anesthesia Workstation", "name_ar": "محطة التخدير المتكاملة",
        "tagline_en": "Integrated gas delivery & ventilation", "tagline_ar": "توصيل غازات وتهوية متكاملة",
        "image": f"{U}/photo-1519494026892-80bbd2d6fd0d?{IMG}",
        "description_en": "A complete anesthesia platform combining ventilator, vaporizers and patient monitoring in one tower. Low-flow capabilities and agent monitoring reduce gas consumption and enhance safety.",
        "description_ar": "منصة تخدير كاملة تجمع جهاز التنفس وأجهزة التبخير ومراقبة المريض في برج واحد. قدرات التدفق المنخفض ومراقبة الغاز المخدر تقللان الاستهلاك وترفعان مستوى السلامة.",
        "principle_en": "Medical gases (O2, N2O, air) are mixed and passed through a vaporizer that adds precise anesthetic concentrations. The mixture flows into the patient circuit with a soda-lime absorber scrubbing exhaled CO2, while the ventilator maintains controlled or assisted breathing.",
        "principle_ar": "تُمزج الغازات الطبية (الأكسجين وآكسيد النيتروز والهواء) وتمر عبر جهاز التبخير الذي يضيف تراكيز دقيقة من المخدر، ثم يتدفق الخليط إلى دائرة المريض حيث يمتص الجير الصودي ثاني أكسيد الكربون الزفيري، بينما يحافظ جهاز التنفس على تنفس مضبوط أو مساعَد.",
        "components": [
            {"en": "Gas mixing & flow control bank", "ar": "مجموعة مزج الغازات والتحكم بالتدفق"},
            {"en": "Dual selective vaporizers", "ar": "مبخرتان انتقائيتان"},
            {"en": "Integrated ventilator bellows", "ar": "منفاخ التنفس المدمج"},
            {"en": "Circle absorber (CO2) system", "ar": "نظام الامتصاص الدائري لثاني أكسيد الكربون"},
            {"en": "Agent & gas analyzer", "ar": "محلل الغاز المخدر والغازات"},
            {"en": "Integrated patient monitor", "ar": "شاشة مراقبة المريض المدمجة"},
        ],
        "specs": [
            {"label_en": "Vaporizer slots", "label_ar": "منافذ المبخرات", "value": "2"},
            {"label_en": "Fresh gas flow", "label_ar": "تدفق الغاز الطازج", "value": "0.1–15 L/min"},
            {"label_en": "Ventilation modes", "label_ar": "أنماط التهوية", "value": "8"},
            {"label_en": "Battery backup", "label_ar": "البطارية الاحتياطية", "value": "90 min"},
        ],
    },
    {
        "id": "surg-robot", "category": "surgical", "department": "operating_room", "price": 1800000,
        "name_en": "Robotic Surgery System", "name_ar": "نظام الجراحة الروبوتية",
        "tagline_en": "Four-arm minimally invasive platform", "tagline_ar": "منصة جراحة طفيفة التوغل بأربعة أذرع",
        "image": f"{U}/photo-1551601651-2a8555f1a136?{IMG}",
        "description_en": "A master-slave robotic platform translating a surgeon's hand movements into tremor-filtered, scaled micro-motions inside the patient. Immersive 3D-HD vision and wristed instruments redefine minimally invasive surgery.",
        "description_ar": "منصة روبوتية رئيسية-تابعة تحوّل حركات يد الجراح إلى حركات دقيقة مصفّاة من الرعشة ومضبوطة المقياس داخل جسم المريض. رؤية ثلاثية الأبعاد غامرة وأدوات ذات معصم مفصلي تعيد تعريف الجراحة طفيفة التوغل.",
        "principle_en": "The surgeon operates from an ergonomic console viewing a magnified 3D operative field. Sensors capture hand and finger motion; computers filter tremor, scale movement (e.g. 5:1) and drive robotic arms holding wristed instruments through keyhole ports.",
        "principle_ar": "يعمل الجراح من وحدة تحكم مريحة مع رؤية مجسمة مكبرة لحقل العملية؛ تلتقط المستشعرات حركة اليد والأصابع، وتصفّي الحواسيب الرعشة وتضبط مقياس الحركة (مثل 5:1) وتقود الأذرع الروبوتية الحاملة لأدوات مفصلية عبر فتحات صغيرة.",
        "components": [
            {"en": "Surgeon console (3D viewer)", "ar": "وحدة تحكم الجراح (عرض ثلاثي الأبعاد)"},
            {"en": "Patient-side cart with 4 arms", "ar": "عربة جانب المريض بأربعة أذرع"},
            {"en": "EndoWrist articulating instruments", "ar": "أدوات مفصلية المعصم"},
            {"en": "3D-HD endoscope camera", "ar": "كاميرا منظار ثلاثية الأبعاد عالية الدقة"},
            {"en": "Motion-scaling control computers", "ar": "حواسيب التحكم بضبط الحركة"},
            {"en": "Vision & insufflation tower", "ar": "برج الرؤية والنفخ"},
        ],
        "specs": [
            {"label_en": "Robotic arms", "label_ar": "الأذرع الروبوتية", "value": "4"},
            {"label_en": "Degrees of freedom", "label_ar": "درجات الحرية", "value": "7 per arm"},
            {"label_en": "Vision", "label_ar": "الرؤية", "value": "3D HD 10×"},
            {"label_en": "Motion scaling", "label_ar": "ضبط الحركة", "value": "up to 5:1"},
        ],
    },
    {
        "id": "dialysis-hd", "category": "life_support", "department": "nephrology", "price": 22000,
        "name_en": "Hemodialysis Machine", "name_ar": "جهاز غسيل الكلى",
        "tagline_en": "Extracorporeal renal replacement", "tagline_ar": "تعويض كلوي خارج الجسم",
        "image": f"{U}/photo-1638202993928-7267aad84c31?{IMG}",
        "description_en": "A single-patient hemodialysis system with online clearance monitoring and ultrafiltration profiling. Touch-guided setup, automatic disinfection and bicarbonate cartridge support.",
        "description_ar": "نظام غسيل كلوي لمريض واحد مع مراقبة فورية للتصفية وملامح الترشيح الفائق. إعداد موجّه باللمس وتعقيم آلي ودعم خراطيش البيكربونات.",
        "principle_en": "Blood is pumped through a dialyzer — thousands of hollow fibers acting as a semi-permeable membrane. Dialysate flowing counter-currently draws urea, toxins and excess electrolytes out by diffusion, while controlled ultrafiltration removes surplus water before clean blood returns to the patient.",
        "principle_ar": "يُضخ الدم عبر المُرشّح الدموي — آلاف الألياف المجوفة التي تعمل كغشاء شبه نفوذ. يجري السائل الديالي بعكس الاتجاه ساحباً اليوريا والسموم والشوارد الزائدة بالانتشار، بينما يزيل الترشيح الفائق المضبوط الماء الفائض قبل عودة الدم النظيف إلى المريض.",
        "components": [
            {"en": "Blood pump & arterial/venous lines", "ar": "مضخة الدم والخطان الشرياني والوريدي"},
            {"en": "Hollow-fiber dialyzer", "ar": "المرشح الدموي بالألياف المجوفة"},
            {"en": "Dialysate proportioning system", "ar": "نظام تعيير السائل الديالي"},
            {"en": "Heparin infusion pump", "ar": "مضخة حقن الهيبارين"},
            {"en": "Air detector & venous clamp", "ar": "كاشف الهواء والمشبك الوريدي"},
            {"en": "Disinfection & rinse module", "ar": "وحدة التعقيم والشطف"},
        ],
        "specs": [
            {"label_en": "Blood flow", "label_ar": "تدفق الدم", "value": "50–600 mL/min"},
            {"label_en": "Dialysate flow", "label_ar": "تدفق السائل", "value": "300–800 mL/min"},
            {"label_en": "UF precision", "label_ar": "دقة الترشيح", "value": "±1%"},
            {"label_en": "Session time", "label_ar": "زمن الجلسة", "value": "3–5 h"},
        ],
    },
    {
        "id": "hema-analyzer", "category": "laboratory", "department": "laboratory", "price": 35000,
        "name_en": "Auto Hematology Analyzer", "name_ar": "محلل الدم الآلي",
        "tagline_en": "60-sample/hour CBC with 5-part diff", "tagline_ar": "تحليل دم شامل بمعدل 60 عينة/ساعة",
        "image": f"{U}/photo-1587854692152-cbe660dbde88?{IMG}",
        "description_en": "A benchtop hematology analyzer delivering 29-parameter complete blood counts with 5-part WBC differentiation. Closed-tube sampling, auto-loader and laboratory-information-system connectivity.",
        "description_ar": "محلل أمراض دم مكتبي يقدم تعداد دم شامل بـ29 معياراً مع تفريق خماسي لكريات الدم البيضاء. سحب عينات من أنابيب مغلقة ومحمّل آلي وربط بنظام معلومات المختبر.",
        "principle_en": "Blood samples are aspirated, diluted and lysed, then passed through impedance apertures that count and size cells (Coulter principle). Laser flow cytometry and chemical staining classify white-cell subtypes, while cyanide-free photometry measures hemoglobin.",
        "principle_ar": "تُسحب عينات الدم وتُخفف وتُحلل ثم تمر عبر فتحات المقاومة الكهربائية التي تعد الخلايا وتقيس أحجامها (مبدأ كولتر)، بينما تصنف قياسات التدفق الليزري والصبغ الكيميائي أنواع الكريات البيضاء، ويقيس القياس الضوئي الخالي من السيانيد الهيموغلوبين.",
        "components": [
            {"en": "Auto-loader sample rack", "ar": "حامل العينات الآلي"},
            {"en": "Aspiration probe & diluter", "ar": "مجس السحب والمخفف"},
            {"en": "Impedance counting apertures", "ar": "فتحات العد بالمقاومة"},
            {"en": "Laser flow-cytometry bench", "ar": "منصة قياس التدفق الليزري"},
            {"en": "Reagent pack (diluent, lyse)", "ar": "حزمة الكواشف (مخفف، محلل)"},
            {"en": "LIS-connected analysis computer", "ar": "حاسوب التحليل المتصل بنظام المختبر"},
        ],
        "specs": [
            {"label_en": "Throughput", "label_ar": "الإنتاجية", "value": "60 tests/h"},
            {"label_en": "Parameters", "label_ar": "المعايير", "value": "29"},
            {"label_en": "Sample volume", "label_ar": "حجم العينة", "value": "20 µL"},
            {"label_en": "Storage", "label_ar": "التخزين", "value": "100,000 results"},
        ],
    },
]

CATEGORIES = [
    {"key": "imaging", "en": "Imaging", "ar": "التصوير الطبي"},
    {"key": "monitoring", "en": "Monitoring", "ar": "المراقبة"},
    {"key": "life_support", "en": "Life Support", "ar": "إنقاذ الحياة"},
    {"key": "surgical", "en": "Surgical", "ar": "الجراحة"},
    {"key": "laboratory", "en": "Laboratory", "ar": "المختبر"},
    {"key": "diagnostics", "en": "Diagnostics", "ar": "التشخيص"},
]

DEPARTMENTS = [
    {"key": "radiology", "en": "Radiology", "ar": "الأشعة"},
    {"key": "icu", "en": "ICU", "ar": "العناية المركزة"},
    {"key": "operating_room", "en": "Operating Room", "ar": "غرفة العمليات"},
    {"key": "laboratory", "en": "Laboratory", "ar": "المختبر"},
    {"key": "cardiology", "en": "Cardiology", "ar": "القلب"},
    {"key": "emergency", "en": "Emergency", "ar": "الطوارئ"},
    {"key": "nephrology", "en": "Nephrology", "ar": "الكلى"},
    {"key": "ward", "en": "Ward", "ar": "الأجنحة"},
    {"key": "clinic", "en": "Clinic", "ar": "العيادات"},
]

PROJECTION = {"_id": 0}


@app.on_event("startup")
async def seed_devices():
    await db.devices.create_index("id", unique=True)
    if await db.devices.count_documents({}) == 0:
        await db.devices.insert_many([dict(d) for d in DEVICES])
        logger.info("Seeded %d devices", len(DEVICES))
    else:
        for d in DEVICES:
            await db.devices.replace_one({"id": d["id"]}, dict(d), upsert=True)


@api_router.get("/")
async def root():
    return {"message": "MedAtlas API"}


@api_router.get("/meta")
async def get_meta():
    prices = [d["price"] for d in DEVICES]
    return {
        "categories": CATEGORIES,
        "departments": DEPARTMENTS,
        "price_min": min(prices),
        "price_max": max(prices),
        "count": await db.devices.count_documents({}),
    }


@api_router.get("/devices")
async def list_devices(
    search: Optional[str] = None,
    category: Optional[str] = None,
    department: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort: str = "featured",
):
    query: dict = {}
    if search:
        query["$or"] = [
            {"name_en": {"$regex": search, "$options": "i"}},
            {"name_ar": {"$regex": search, "$options": "i"}},
            {"tagline_en": {"$regex": search, "$options": "i"}},
            {"tagline_ar": {"$regex": search, "$options": "i"}},
        ]
    if category:
        query["category"] = category
    if department:
        query["department"] = department
    price_q: dict = {}
    if min_price is not None:
        price_q["$gte"] = min_price
    if max_price is not None:
        price_q["$lte"] = max_price
    if price_q:
        query["price"] = price_q

    sort_map = {
        "price_asc": [("price", 1)],
        "price_desc": [("price", -1)],
        "name": [("name_en", 1)],
    }
    cursor = db.devices.find(query, PROJECTION)
    if sort in sort_map:
        cursor = cursor.sort(sort_map[sort])
    return await cursor.to_list(200)


@api_router.get("/devices/{device_id}")
async def get_device(device_id: str):
    device = await db.devices.find_one({"id": device_id}, PROJECTION)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

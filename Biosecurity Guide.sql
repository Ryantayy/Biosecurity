DROP SCHEMA IF EXISTS biosecurity;
CREATE SCHEMA biosecurity;
USE biosecurity;

CREATE TABLE IF NOT EXISTS user (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  role ENUM('agronomist', 'staff', 'admin') NOT NULL,
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS agronomist (
  agronomist_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  address VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
  phone_number VARCHAR(20),
  date_joined DATE NOT NULL,
  status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
  PRIMARY KEY (agronomist_id),
  UNIQUE (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS staffadmin (
  staff_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  email VARCHAR(255) NOT NULL UNIQUE,
  work_phone_number VARCHAR(20),
  hire_date DATE,
  position VARCHAR(45),
  department VARCHAR(45),
  status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
  FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
  PRIMARY KEY (staff_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS pest_directory (
  agriculture_id INT NOT NULL AUTO_INCREMENT,
  item_type ENUM('pest', 'weed') NOT NULL,
  common_name VARCHAR(100) NOT NULL,
  scientific_name VARCHAR(100),
  key_characteristics TEXT,
  biology_description TEXT,
  impacts TEXT,
  control TEXT,
  primary_image VARCHAR(255),
  additional_image VARCHAR(255),
  PRIMARY KEY (agriculture_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/* Insert 9 users into user table */
INSERT INTO user (username, password, email, role) VALUES 
('ryan', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'ryan@gmail.com', 'agronomist'),
('ray', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'ray@gmail.com', 'agronomist'),
('lukia', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'lukia@gmail.com', 'agronomist'),
('luna', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'luna@gmail.com', 'agronomist'),
('lina', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'lina@gmail.com', 'agronomist'),
('lana', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'lana@gmail.com', 'staff'),
('leila', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'leila@gmail.com', 'staff'),
('lycan', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'lycan@gmail.com', 'staff'),
('byan', 'eea689028ca0cbc7fc4f1bd824b1b9ed419bb5720565e364003a24e16aff1d3c', 'byan@gmail.com', 'admin');

/* Insert 5 agronomists into the agronomist table */
INSERT INTO agronomist (user_id, first_name, last_name, address, email, phone_number, date_joined, status)
SELECT 
    user_id, 
    CASE email 
        WHEN 'ryan@gmail.com' THEN 'Ryan'
        WHEN 'ray@gmail.com' THEN 'Ray'
        WHEN 'lukia@gmail.com' THEN 'Lukia'
        WHEN 'luna@gmail.com' THEN 'Luna'
        WHEN 'lina@gmail.com' THEN 'Lina'
    END, 
    CASE email 
        WHEN 'ryan@gmail.com' THEN 'Tay'
        WHEN 'ray@gmail.com' THEN 'Lee'
        WHEN 'lukia@gmail.com' THEN 'Swift'
        WHEN 'luna@gmail.com' THEN 'Moofung'
        WHEN 'lina@gmail.com' THEN 'Inverse'
    END, 
    '123 Abc Ave', -- Assuming same address for simplification
    email, 
    CASE email 
        WHEN 'ryan@gmail.com' THEN '555-0102'
        WHEN 'ray@gmail.com' THEN '555-0103'
        WHEN 'lukia@gmail.com' THEN '555-0104'
        WHEN 'luna@gmail.com' THEN '555-0105'
        WHEN 'lina@gmail.com' THEN '555-0106'
    END, -- Unique phone numbers
    CURDATE(), -- Assuming the current date for date_joined
    'active'
FROM user 
WHERE role = 'agronomist';

/* Insert 3 staff and 1 admin details into staff_admin table */
INSERT INTO staffadmin (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status)
SELECT user_id, 'Lana', 'Doe', email, '888-0101', '2020-02-09', 'Staff', 'Management', 'active'
FROM user WHERE email = 'lana@gmail.com'
UNION
SELECT user_id, 'Leila', 'Smith', email, '888-0102', '2021-01-01', 'Staff', 'Operation', 'active'
FROM user WHERE email = 'leila@gmail.com'
UNION
SELECT user_id, 'Lycan', 'Wolf', email, '888-0103', '2022-02-02', 'Staff', 'Operation', 'active'
FROM user WHERE email = 'lycan@gmail.com'
UNION
SELECT user_id, 'Byan', 'King', email, '888-0104', '2023-03-03', 'Admin', 'Management', 'active'
FROM user WHERE email = 'byan@gmail.com';

INSERT INTO pest_directory (agriculture_id, item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control, primary_image, additional_image) VALUES
(1, 'pest', 'Argentine stem weevil adult', 'Listronotus bonariensis', 'Argentine stem weevil Adults are small (2-3 mm) and have a dark elongated body. Active during warm months. Larvae feed inside grass stems, causing significant damage.', '- Argentine stem weevil (Listronotus bonariensis) adults are most active during warm months, laying eggs in grass stems. The larvae phase is critical, as it directly feeds on the inside of the grass stems, potentially stunting or killing the plant.', 'Adult feeding is characterised by “windowing” effects on the leaves, while larval damage can significantly reduce grass growth and vigor, impacting agricultural productivity.', 'Insecticide applications may be necessary for control, alongside monitoring and cultural practices to manage populations.', 'Argentine-stem-weevil-web.jpg', 'Argentine-stem-weevil-adult-2.jpg'),
(2, 'pest', 'Black field cricket', 'Teleogryllus commodus', 'Black crickets are found throughout the North and South Islands, preferring dry, open habitats. Adults can grow up to 2.5 cm long.', 'Adult black field crickets are about 2.5 cm long, with females being larger than males. They are nocturnal and are most active during warm, humid nights.', 'Black field crickets are generally pests only under dry conditions, damaging pastures, crops, and vegetables by feeding on or cutting young plants.', 'Chemical control is advised for populations of more than 10 crickets per square meter, with baiting as an effective method.', 'Black-field-cricket.jpg', 'Black-field-cricket2.jpg'),
(3, 'pest', 'Clover Root Weevil', 'Sitona obsoletus', 'Major pest of clovers, both red and white cultivated varieties. Adults are mahogany-brown with a distinctive snout.', 'Clover root weevil (CRW) adults are mahogany-brown with a distinctive snout, feeding on clover leaves. The larvae feed on the roots, causing significant damage.', 'Feeding by adult CRW causes distinctive semi-circular notches on the leaf edges, while larval feeding on roots reduces nitrogen fixation and plant growth.', 'Insecticides during pasture establishment and biological control using a parasitic wasp have shown effectiveness.', 'Clover-root-weevil-adult.jpg', 'Adult-clover-root-weevil.jpg'),
(4, 'pest', 'Diamondback moth', 'Plutella xylostella', 'Pest of all brassica crops, found throughout New Zealand. The caterpillars feed on leaves, creating significant damage.', 'Diamondback moth is common throughout the country, especially in areas growing brassica crops. The caterpillars feed on the leaves, causing holes.', 'Diamondback moth caterpillars feed on all brassicas, causing holes and reducing crop quality and yield.', 'Biological control agents, such as the wasp Diadegma semiclausum, have been introduced to control populations naturally.', 'Diamondback-moth-caterpillar-and-feeding-scars.jpg', 'Diamondback-moth-caterpillar-and-feeding-scars2.jpg'),
(5, 'pest', 'Greasy cutworm', 'Agrotis ipsilon', 'Found throughout agricultural areas of New Zealand, the greasy cutworm attacks a wide range of plants. The larvae are particularly damaging.', 'Moths can be found year round but are most common from late summer to autumn. The larvae, which do the most damage, feed at night, cutting off young plants at ground level.', 'The larger caterpillars are the most damaging, feeding at night and cutting young plants at ground level, which can significantly impact crop establishment.', 'Thorough cultivation and good weed control, alongside monitoring and appropriate insecticide use, can manage cutworm populations.', 'Greasy-cutworm-adult3_James.jpg', '3-cutworm-larva-damage.jpg'), 
(6, 'pest', 'Plantain moth', 'Scopula rubraria and Epyaxa rosearia', 'Consists of at least 2 species which may be difficult to differentiate. They have pale brownish to greenish forewings with wavy lines.', 'Very little is known about the biology of these moths. They are assumed to have similar life cycles to other pasture moths.', 'The caterpillars feed on the plant leaves causing windowing and notches similar to grass grub and porina damage.', 'There are no registered insecticides for control. Management relies on general pasture management.', 'Epyaxa-rosearia2_James.jpg', 'Plantain-moth-on-Moth-on-Tonic-plantain.jpg'),
(7, 'pest', 'Porina', 'Moths fly in large numbers during spring and early summer', 'Specific key characteristics are not detailed.', 'Porina are a complex of caterpillars occurring in pastures. Moths fly in large numbers during spring and early summer.', 'Porina are grazers. At low densities, they are beneficial but can cause damage at high populations.', 'Assessing populations and managing accordingly. There are no specific control products mentioned.', 'Porina-Small-1-web.jpg', 'Porina-Large-1-web.jpg'),
(8, 'pest', 'Redheaded pasture cockchafer', 'Adoryphorus coulonii', 'Redheaded pasture cockchafer is currently restricted to Central Otago. It is a native beetle with a distinctive red head.', 'The redheaded pasture cockchafer is an Australian native that has become established in Central Otago.', 'Larvae feed on organic matter and plant roots, causing damage to pasture.', 'Few control options are available, with a focus on monitoring and understanding the beetle’s life cycle.', 'Redheaded-pasture-cockchafer-beetles-1.jpg', 'Redheaded-pasture-cockchafer-beetles-2.jpg'),
(9, 'pest', 'Sod webworm', 'Eudonia sabulosella', 'Sod webworms are caterpillars of several native moth species. They have a pale brown color and create silk-lined tunnels.', 'There are numerous species of caterpillars grouped as sod webworms. They are active at night and cause damage to pastures.', 'They cause damage to a variety of pasture plants by feeding on the leaves.', 'No specific control measures are listed; damage is typically managed through pasture management.', 'Sod-Web-worth-4-web.jpg', 'Sod-Web-worm-web.jpg'),
(10, 'pest', 'White butterfly, cabbage white butterfly', 'Pieris rapae', 'Butterflies are white with one or two black spots on the wings. They are a common sight in gardens and fields.', 'The white butterfly is common throughout the country and can be seen fluttering around gardens and crops.', 'Caterpillars feed on brassicas and can cause significant damage to crops.', 'Biological control agents and generalist predators are used to manage populations.', 'Cabbage-white-caterpillar-March-16-Mosgiel-IMG_6541.jpg', 'Cabbage-white-caterpillar2.jpg'),
(11, 'weed', 'Alligator Weed', 'Alternanthera philoxeroides', 'Low-growing, perennial with long horizontal stems, shiny leaves, and small white flower heads. Stems can grow up to 60 cm high, with hollow internodes.', 'Originates from Brazil, known as a major weed in several countries. Reproduces vegetatively and can survive frost under protection. Thrives in nutrient-rich and slightly brackish water.', 'Rapidly out-competes crops and pastures, toxic to some livestock, and can clog waterways increasing flooding risks. Illegal to propagate in New Zealand.', 'Control by ensuring equipment is clean, using weed-free feed, and applying relevant herbicides to prevent spread.', 'alligator-weed.jpg', 'Alligator-Weed-4.jpg'),
(12, 'weed', 'Barley grass', 'Critesion spp', 'Annual grass that germinates in autumn. Seeds have bristly awns and leaves have a short, white, toothed ligule.', 'Native to the Mediterranean and parts of Asia. Germinates in autumn, minimal seed dormancy. Provides quality feed in the vegetative stage.', 'Competes in pastures, especially on high fertility soil. Awned seeds can damage livestock and reduce growth rates.', 'Control includes maintaining healthy pasture, herbicide application, and possibly reseeding affected areas.', 'barley-grass.jpg', 'Barley-grass-2.jpg'),
(13, 'weed', 'Blackberry', 'Rubus fruticosus', 'Prickly shrub with long branches, sharp thorns, and edible berries. Leaves have five to seven leaflets.', 'Introduced for hedgerows and soil control, now invasive, smothering native vegetation and problematic in pastures.', 'Reduces stock-carrying capacity and can entangle and kill livestock.', 'Control with grazing management, manual removal, herbicides, and spreading rust to vulnerable plants.', 'blackberry-flowers.jpg', 'Blackberry-fruit.jpg'),
(14, 'weed', 'Bracken', 'Pteridium esculentum', 'Native fern with underground stems, erect glossy stalks, and spore-bearing organs on leaf undersides. Can grow up to 4 m on forest margins.', 'Reproduces by spores, increased after human forest clearing. Used historically by Maori as food.', 'Forms dense cover, uses soil nutrients, toxic to livestock, and competes with young trees.', 'Control includes mowing, establishing competitive pasture species, and selective herbicide application.', 'Pteridium-esculentum-b-default-picture1.jpg', 'Pteridium-esculentum-e1-700x467.jpg'),
(15, 'weed', 'Broom corn millet', 'Panicum miliaceum', 'Broad leaves resembling maize, with long hairs on sheath. Flower spikelets on branched panicles and shiny seeds.', 'Originally a crop for human consumption, now a wild biotype emerged as a weed. Germinates with warm season, rapid growth.', 'Reduces crop yields by competing for water, nutrients, and sunlight. Interferes with harvesting machinery.', 'No specific control methods provided, implies managing competition and harvest issues.', 'Broom-corn-millet-seed-head.jpg', 'Broom-corn-millet.jpg'),
(16, 'weed', 'Cape weed', 'Arctotheca calendula', 'Annual with a rosette of greyish-green lobed leaves, woolly undersides, and yellow flowers with a dark purple center. Similar to Gazania and African daisy.', 'Native to South Africa, common in the North Island and parts of the South Island. Produces large amounts of seed, adapted to most soil types.', 'Smothers desirable pasture species, difficult for cattle to graze, and potentially toxic due to high nitrate levels.', 'Control through grazing management, chemical application (clopyralid, dicamba, picloram), and maintaining dense turf to prevent establishment.', 'Arctotheca-calendula-ap.jpg', 'Arctotheca-calendula-ak.jpg'),
(17, 'weed', 'Dandelion', 'Taraxacum officinale', 'Perennial with a leafless, hollow stem and large yellow flower. Basal leaves are thin, smooth, with teeth pointing towards the base.', 'Native to Eurasia, flowers from early spring to autumn. Seeds dispersed by wind.', 'Thrives in dairy pastures, reducing crop yields and slowing hay drying.', 'Control by grazing management and chemical control (MCPA, 2,4-D) at the vegetative stage.', 'Dandelion-3.jpg', 'Dandelion-6.jpg'),
(18, 'weed', 'Giant buttercup', 'Ranunculus acris', 'Perennial up to 1m tall with yellow glossy flowers and highly variable leaves. Common in dairy pastures in high-rainfall areas.', 'Introduced from Europe, reproduces via seeds and daughter rhizomes.', 'Reduces pasture’s stock-carrying capacity and can cause milk solids production loss.', 'Grazing management with sheep, grubbing/mowing before flowering, and chemical control with aminopyralid or triclopyr.', 'Giant-buttercup-flower.jpg', 'Giant-buttercup.jpg'),
(19, 'weed', 'Hemlock', 'Conium maculatum', 'Tall, foul-smelling, with purple-spotted stems and small white flowers. All parts are poisonous.', 'Native to Europe, Asia, and North Africa, common in waste places and damp areas in NZ.', 'Toxic to humans and livestock, can cause death.', 'Control by grazing management, mowing, and chemical control (2,4-D, flumetsulam) without harming pasture components.', 'Conium-maculatum-ab.jpg', 'Conium-maculatum-k.jpg'),
(20, 'weed', 'Ragwort', 'Jacobaea vulgaris', 'Biennial or perennial with bright yellow flowers and a fibrous root system. Forms a dense rosette in its first year.', 'Originated from Europe, Asia, and Siberia. Produces over 50,000 seeds, some lasting up to 20 years.', 'Alkaloid compounds are poisonous, damaging to the liver of horses and cattle. Toxic to deer and causes milk and honey taint.', 'Control by grazing management, chemical control (2,4-D, dicamba, triclopyr/picloram), mowing or grubbing, and integrated pest management.', 'Ragwort-flower.jpg', 'Ragwort-plant.jpeg');


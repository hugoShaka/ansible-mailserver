INSERT INTO virtual_domains VALUES (1, 'sith.local');
INSERT INTO virtual_domains VALUES (2, 'jedi.local');

INSERT INTO virtual_users VALUES (1, 1, '{SHA512-CRYPT}$6$fysxPW0xNM5dMZ.z$xlsrVtdnh7wLPj2G1x3EpfPvnA5Yn.vtkna03s2EvPDryM9HWjEnMj1JcEGuSaQy3mGSPIiPH7jPyQTEYH1VL0', 'sidious');
INSERT INTO virtual_users VALUES (2, 2, '{SHA512-CRYPT}$6$fysxPW0xNM5dMZ.z$xlsrVtdnh7wLPj2G1x3EpfPvnA5Yn.vtkna03s2EvPDryM9HWjEnMj1JcEGuSaQy3mGSPIiPH7jPyQTEYH1VL0', 'obiwan');
INSERT INTO virtual_users VALUES (3, 1, '{SHA512-CRYPT}$6$fysxPW0xNM5dMZ.z$xlsrVtdnh7wLPj2G1x3EpfPvnA5Yn.vtkna03s2EvPDryM9HWjEnMj1JcEGuSaQy3mGSPIiPH7jPyQTEYH1VL0', 'vader');
-- password is 'test'

INSERT INTO virtual_aliases VALUES (1, 2, 'skywalker', 'vader@sith.local');
INSERT INTO virtual_aliases VALUES (2, 1, 'external-alias', 'user@test.not.local');


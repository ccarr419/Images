import lxml.etree as ET
import sys
def main():
    xml = sys.argv[1]
    #print xml
    #xml = "<?xml version='1.0' encoding='UTF-8'?><GMOOH><Checksheet><Section><SectionNo>1</SectionNo><SectionDesc>I. UNIVERSITY CORE (12 credits)</SectionDesc><Pos><PosDesc>A.Oral Communication:</PosDesc><ReqInst><Dept>COM</Dept><ClassNums>10 or above</ClassNums></ReqInst></Pos><Pos><PosDesc>B.Written Communication:</PosDesc><ReqInst><Dept>ENG</Dept><ClassNums>23 - 25</ClassNums></ReqInst></Pos><Pos><PosDesc>C.Mathematics:</PosDesc><ReqInst><Dept>MAT</Dept><ClassNums>17 or above</ClassNums></ReqInst></Pos><Pos><PosDesc>D.Wellness:</PosDesc><ReqInst><Dept>HEA</Dept><ClassNums>Any</ClassNums></ReqInst></Pos></Section><Section><SectionNo>2</SectionNo><SectionDesc>II. UNIVERSITY DISTRIBUTION (15 credits)</SectionDesc><Pos><PosDesc>A.Natural Sciences:</PosDesc><ReqInst><Dept>AST</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>BIO</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>CHM</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ENV</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>GEL</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>MAR</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>NSE</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>PHY</Dept><ClassNums>Any</ClassNums></ReqInst></Pos><Pos><PosDesc>B.Social Sciences:</PosDesc><ReqInst><Dept>PSY</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ANT</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>CRJ</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ECO</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>HIS</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>INT</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>MCS</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>PSY</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>POL</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>SOC</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>SSE</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>SWK</Dept><ClassNums>Any</ClassNums></ReqInst></Pos><Pos><PosDesc>C.Humanities:</PosDesc><ReqInst><Dept>ENG</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ENG</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ENG</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>HUM</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>PAG</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>PHI</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>WRI</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>WGS</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>Modern Language</Dept><ClassNums>Any</ClassNums></ReqInst></Pos><Pos><PosDesc>D.Arts:</PosDesc><ReqInst><Dept>ARC</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ARH</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>ART</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>CDE</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>CDH</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>CFT</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>DAN</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>FAR</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>FAS</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>MUP</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>MUS</Dept><ClassNums>Any</ClassNums></ReqInst><ReqInst><Dept>THE</Dept><ClassNums>Any</ClassNums></ReqInst></Pos></Section></Checksheet><Checksheet><Program><ProgramTitle>BS Computer Science: Information Technology</ProgramTitle><ProgramNo>ULASCSCIT</ProgramNo><ProgramVersion>2118</ProgramVersion><ProgramAbriv>COMPUTER SCIENCE: IT</ProgramAbriv><ProgramNotes>Consider taking a Minor in an Application Domain such as Math, Psychology, Sociology, Economics, Biology, or any ScienceConsider taking a second speech course in II ECSC-prefix courses below 125-level, CSC 280 and CSC 380 do not count toward the BS in Information TechnologyBefore taking any 300-level course a student must have completed 18 credit hours in CSC courses numbered 125 or above with a GPA of 2.25 in the CSC courses.</ProgramNotes><Column><ColumnDesc>B. Major Program: 57 sh</ColumnDesc><Section><SectionDesc>1. Required Courses: 33 sh</SectionDesc><Class><ClassID>1</ClassID><ClassDept>1</ClassDept><ClassNo>1</ClassNo><ClassDesc>1</ClassDesc></Class><Class><ClassID>2</ClassID><ClassDept>2</ClassDept><ClassNo>2</ClassNo><ClassDesc>2</ClassDesc></Class><Class><ClassID>3</ClassID><ClassDept>3</ClassDept><ClassNo>3</ClassNo><ClassDesc>3</ClassDesc></Class><Class><ClassID>4</ClassID><ClassDept>4</ClassDept><ClassNo>4</ClassNo><ClassDesc>4</ClassDesc></Class></Section><Section><SectionDesc>2. Elective Courses: 15-24 sh</SectionDesc><Class><ClassID>5</ClassID><ClassDept>5</ClassDept><ClassNo>5</ClassNo><ClassDesc>5</ClassDesc></Class></Section><Section><SectionDesc>3. Elective Courses: 0-9 sh</SectionDesc></Section></Column><Column><ColumnDesc>C. Concomitant Courses: 3 sh</ColumnDesc><Section><SectionDesc>1. Required Courses: 3 sh</SectionDesc><Class><ClassID>100</ClassID><ClassDept>6</ClassDept><ClassNo>6</ClassNo><ClassDesc>6</ClassDesc></Class><Class><ClassID>101</ClassID><ClassDept>7</ClassDept><ClassNo>7</ClassNo><ClassDesc>7</ClassDesc></Class></Section><Section><SectionDesc>2. Internship optional (free elective)</SectionDesc></Section></Column></Program></Checksheet></GMOOH>"
    dom = ET.fromstring(xml)
    xslt = ET.parse("testcheck.xsl")
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    return ET.tostring(newdom, pretty_print=True)
    
if __name__ == '__main__':
    sys.stdout.write(main())
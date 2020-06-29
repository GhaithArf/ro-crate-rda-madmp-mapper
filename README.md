# RO-Crate RDA maDMP Mapper


[![DOI](https://zenodo.org/badge/262980184.svg)](https://zenodo.org/badge/latestdoi/262980184)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/GhaithArf/ro-crate-rda-madmp-mapper/blob/master/LICENSE)


``` Ro-Crate RDA maDMP Mapper ``` is a tool that defines mapping between [RO-Crate](https://researchobject.github.io/ro-crate/) and 
[RDA maDMP](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard). It allows generating RO-Crate(s) from maDMP (1 to many) and 
maDMP from RO-Crate(s) (many to 1).

## Mapping

### Assumptions

<p>
  DMPs can include multiple datasets. However, ro-crate include only one
  dataset. The dataset can include other nested datasets. It is assumed that
  most of the data for the dataset at the root (e.g. funding, contributors,
  authors,...) is equivalent to the data of DMP. Nested datasets will be
  included as elements of distributions.
</p>
<p>
  RO-crates have to have @id for each property. Otherwise, the jsonld generated
  would have a wrong format. However, an identifier is not always present for
  entities of DMP. In case of absence of identifiers, it is assumed that the
  title is also the @id.
</p>
<p>
  The website of ro-crate explicitly mentions that it is possible to use
  schema.org metadata to supplement RO-Crate. So, if there are attributes which
  are present in DMP and missing in ro-crates, they are accounted for by other
  Linked Data Vocabularies. (Example: cost)
</p>

#### Mapped Properties

<table style="width: 99%;">
  <thead>
    <tr>
      <th>ro-crate attribute</th>
      <th>@type of ro-crate property</th>
      <th>DMP attribute</th>
      <th>Parent of DMP attribute</th>
      <th>Comment/Assumption</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">contactPoint</td>
      <td valign="top">ContactPoint</td>
      <td valign="top">contact</td>
      <td valign="top">dmp</td>
      <td valign="top">
        It is assumed that the contact person for the DMP is the same as the
        contact person of the dataset.
      </td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">ContactPoint</td>
      <td valign="top">identifier</td>
      <td valign="top">contact_id</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">email</td>
      <td valign="top">ContactPoint</td>
      <td valign="top">mbox</td>
      <td valign="top">contact</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">ContactPoint</td>
      <td valign="top">name</td>
      <td valign="top">contact</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">contactType</td>
      <td valign="top">ContactPoint</td>
      <td valign="top">type</td>
      <td valign="top">contact</td>
      <td valign="top">
        These attributes are not exactly equivalent. But, they are close enough.
      </td>
    </tr>
    <tr>
      <td valign="top">author/creator</td>
      <td valign="top">Dataset</td>
      <td valign="top">contributor</td>
      <td valign="top">dmp</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">person</td>
      <td valign="top">identifier</td>
      <td valign="top">contributor_id</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">affiliation</td>
      <td valign="top">person</td>
      <td valign="top">role</td>
      <td valign="top">contributor</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">person</td>
      <td valign="top">name</td>
      <td valign="top">contributor</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">email</td>
      <td valign="top">person</td>
      <td valign="top">mbox</td>
      <td valign="top">contributor</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">person</td>
      <td valign="top">identifier</td>
      <td valign="top">contributor_id</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">cost</td>
      <td valign="top">Dataset</td>
      <td valign="top">cost</td>
      <td valign="top">dmp</td>
      <td valign="top">
        In DMP, the cost represents a list of costs related to data management.
        However, the cost for ro-crate may not include all costs.
      </td>
    </tr>
    <tr>
      <td valign="top">costCurrency</td>
      <td valign="top">cost</td>
      <td valign="top">currency_code</td>
      <td valign="top">cost</td>
      <td valign="top">
        This is not explicitly mentioned in ro-crate website. But, cost
        properties can be found in jsonld context used for ro-crates.
      </td>
    </tr>
    <tr>
      <td valign="top">description</td>
      <td valign="top">cost</td>
      <td valign="top">description</td>
      <td valign="top">cost</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">cost</td>
      <td valign="top">title</td>
      <td valign="top">cost</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">value</td>
      <td valign="top">cost</td>
      <td valign="top">value</td>
      <td valign="top">cost</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">Language</td>
      <td valign="top">Dataset</td>
      <td valign="top">language</td>
      <td valign="top">dmp</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">description</td>
      <td valign="top">Dataset</td>
      <td valign="top">description</td>
      <td valign="top">dataset</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">Dataset</td>
      <td valign="top">title</td>
      <td valign="top">dataset</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">identifier</td>
      <td valign="top">Dataset</td>
      <td valign="top">identifier</td>
      <td valign="top">dataset_id</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">Dataset</td>
      <td valign="top">hasPart</td>
      <td valign="top">distribution</td>
      <td valign="top">dataset</td>
      <td valign="top">
        Ro-crates usually include a lot of sub-datasets. They usually include
        information about the main dataset like encoding and size. Therefore,
        they are accounted for as distributions.
      </td>
    </tr>
    <tr>
      <td valign="top">File</td>
      <td valign="top">hasPart</td>
      <td valign="top">distribution</td>
      <td valign="top">dataset</td>
      <td valign="top">
        Ro-crates usually include a lot of sub-Files. Sub-datasets have
        sub-Files. Deeply nested files will not be taken into consideration.
        This is because it does not aline with the concept of distribution.
      </td>
    </tr>
    <tr>
      <td valign="top">downloadUrl</td>
      <td valign="top">DataDownload</td>
      <td valign="top">download_url</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">contentUrl</td>
      <td valign="top">DataDownload</td>
      <td valign="top">access_url</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">endDate</td>
      <td valign="top">DataDownload</td>
      <td valign="top">available_until</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">contentSize</td>
      <td valign="top">Dataset</td>
      <td valign="top">byte_size</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">contentSize</td>
      <td valign="top">Dataset/File</td>
      <td valign="top">byte_size</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">encodingFormat</td>
      <td valign="top">Dataset/File</td>
      <td valign="top">format</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">contentLocation</td>
      <td valign="top">geo_location</td>
      <td valign="top">host</td>
      <td valign="top">
        It is assumed that the name is a country. But, it is not always the
        case. But, it is better than losing th e information.
      </td>
    </tr>
    <tr>
      <td valign="top">title</td>
      <td valign="top">RepositoryObject</td>
      <td valign="top">title</td>
      <td valign="top">host</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">description</td>
      <td valign="top">RepositoryObject</td>
      <td valign="top">description</td>
      <td valign="top">host</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">RepositoryObject</td>
      <td valign="top">url</td>
      <td valign="top">host</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">availability</td>
      <td valign="top">RepositoryObject</td>
      <td valign="top">availability</td>
      <td valign="top">host</td>
      <td valign="top">
        availability is not defined exactly the same for ro-crate and DMP in
        terms of the format of the inputed value.
      </td>
    </tr>
    <tr>
      <td valign="top">license</td>
      <td valign="top">Dataset/File</td>
      <td valign="top">license</td>
      <td valign="top">distribution</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">license</td>
      <td valign="top">license_ref</td>
      <td valign="top">license</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">identifier</td>
      <td valign="top">license</td>
      <td valign="top">license_ref</td>
      <td valign="top">license</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">datePublished</td>
      <td valign="top">Dataset</td>
      <td valign="top">issued</td>
      <td valign="top">dataset</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">keywords</td>
      <td valign="top">Dataset</td>
      <td valign="top">keyword</td>
      <td valign="top">dataset</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">description</td>
      <td valign="top">Organisation</td>
      <td valign="top">description</td>
      <td valign="top">project</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">Organisation</td>
      <td valign="top">title</td>
      <td valign="top">project</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">Organisation</td>
      <td valign="top">title</td>
      <td valign="top">project</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">endDate</td>
      <td valign="top">Organisation</td>
      <td valign="top">end</td>
      <td valign="top">project</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">startDate</td>
      <td valign="top">Organisation</td>
      <td valign="top">start</td>
      <td valign="top">project</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">Grant</td>
      <td valign="top">identifier</td>
      <td valign="top">funder_id</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">@id</td>
      <td valign="top">CreativeWork</td>
      <td valign="top">identifier</td>
      <td valign="top">metadata_standard_id</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">Language</td>
      <td valign="top">CreativeWork</td>
      <td valign="top">language</td>
      <td valign="top">dmp</td>
      <td valign="top">metadata</td>
    </tr>
    <tr>
      <td valign="top">description</td>
      <td valign="top">CreativeWork</td>
      <td valign="top">description</td>
      <td valign="top">dmp</td>
      <td valign="top">metadata</td>
    </tr>
  </tbody>
</table>

#### Unmapped Properties of DMP

<table style="width: 99%;">
  <thead>
    <tr>
      <th>DMP attribute</th>
      <th>Comment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">dmp</td>
      <td valign="top">
        There is no direct mapping to dmp since ro-crate is an approach to
        package research data with their metadata. DMP concept considers the
        bigger picture.
      </td>
    </tr>
    <tr>
      <td valign="top">
        contact_id, contributor_id, dmp_id, dataset_id, hasPart, host, project,
        metadata_standard_id, funder_id
      </td>
      <td valign="top">
        For these attributes, there isn't an equivalent attribute. But, their
        children have equivalent attributes. The equivalence is not needed and
        it is not classified as missing.
      </td>
    </tr>
    <tr>
      <td valign="top">type</td>
      <td valign="top">
        "type" of "contact_id" and "contributor_id" have different meaning than
        "@type". There isn't an equivalent.
      </td>
    </tr>
    <tr>
      <td valign="top">created</td>
      <td valign="top">
        The DMP creation should be at the time the DMP is generated. Therefore,
        it does not have an equivalent in ro-crates.
      </td>
    </tr>
    <tr>
      <td valign="top">modified</td>
      <td valign="top">
        DMP creation date is the same as the modified date in this case.
      </td>
    </tr>
    <tr>
      <td valign="top">
        personal_data, preservation_statement, preservation_statement,
        security_and_privacy, data_access, storage_type, pid_system,
        certified_with, backup_type, backup__frequency,
        ethical_issues_description, ethical_issues_exist, ethical_issues_report,
        data_quality_assurance, sensitive_data
      </td>
      <td valign="top">
        Almost all attributes which have to do with quality, privacy, ethics and
        security are missing in ro-crate and connot be translated. PS:
        accessMode in https://w3id.org/ro/crate/1.0/context is different from
        data_access.
      </td>
    </tr>
    <tr>
      <td valign="top">support_versioning</td>
      <td valign="top">
        This specific attribute has no equivalent in the context. However, there
        is the possibility to include the specific versions with other
        attributes.
      </td>
    </tr>
    <tr>
      <td valign="top">funding_status</td>
      <td valign="top">
        The definition provided in DMP official description does not match any
        of the descriptions for the ro-crate.
      </td>
    </tr>
    <tr>
      <td valign="top">identifier, description, title</td>
      <td valign="top">
        These attributes have to be inputed by the user. It is wrong to assume
        that the DMP's identifier is the same as the dataset's identifier. The
        user should create a new identifier for the DMP. It is also not always
        logical to give the DMP the name of the dataset.
      </td>
    </tr>
  </tbody>
</table>

#### Unmapped Properties of ro-crate

<table style="width: 99%;">
  <thead>
    <tr>
      <th>ro-crate attribute</th>
      <th>Comment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">@context, @graph, conformsTo, about</td>
      <td valign="top">
        There isn't an equivalent for these attributes because they are specific
        to jsonld. However, DMP does not follow jsonld schema. It follows json
        schema. When automatically generating a ro-crate, they are inserted as
        they can be programatically determined. When generating DMPs, they are
        ignored.
      </td>
    </tr>
    <tr>
      <td valign="top">hasPart, hasMember</td>
      <td valign="top">
        DMPs do not have the equivalent of these attributes. However, they are
        accounted for by including their values in distributions.
      </td>
    </tr>
    <tr>
      <td valign="top">publisher, sameAs, temporalCoverage</td>
      <td valign="top">
        These attributes are not included as explicitly in DMPs.
      </td>
    </tr>
    <tr>
      <td valign="top">CreateAction, UpdateAction</td>
      <td valign="top">
        CreateAction and UpdateAction classes are there to model the
        contributions of Context Entities of type Person or Organization. This
        is not present in DMPs.
      </td>
    </tr>
    <tr>
      <td valign="top">latitude, longitude</td>
      <td valign="top">
        Places are described more thouroughly in ro-crates.
      </td>
    </tr>
  </tbody>
</table>


## Usage


In order to map between both standards, the following command should be used:

```python mapper.py -i <input_path> -o <output_path>```

Where ```input_path``` represents a path to the input folder (or file) representing an maDMP or a RO-Crate project and 
```output_path``` represents a path where the generated files will be stored.

It is not required to explicitally define the mapping direction (maDMP to RO-Crate or RO-Crate to maDMP) since this 
is handled within the tool.
x
## Examples

Several maDMP and RO-Crate examples are also provided. They are structured in the following way:
```

├── madmp
│   ├── calculation-of-nice-sunny-days
│   ├── closed
│   ├── dataset-many
│   ├── funded-project
│   ├── life-expectancy-prediction
│   ├── long
│   ├── minimal-content
│   ├── multilayer-perceptron-on-hypothyroid
│   ├── swedish-motor-insurance
│   └── world-development-indicators
└── rocrate
    ├── drug_consumption
    ├── Glop_Pot
    ├── GTM
    ├── NursingResidentStuff
    └── world_development_indicators_visualization
```

For maDMPs, 5 of the examples are taken from examples made by students as part of 
[Data Stewardship](https://tiss.tuwien.ac.at/course/courseDetails.xhtml?dswid=5622&dsrid=420&courseNr=194044) at 
[Vienna University of Technology](https://www.tuwien.at/en/). The other 5 are taken from the examples provided by the 
[RDA-DMP-Common-Standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard/tree/master/examples/JSON).

For RO-Crates, 3 examples are taken from the official [RO-Crate website](https://researchobject.github.io/ro-crate/) 
and the other 2 are especially created to test the coverage of the mapping using existing datasets.

## Demo

A demo of the mapping between both standards can be executed using the following command: 

```python demo.py```


This demo uses the content ```examples``` folder in order to generate mapped files and store them in  ```demo_files```.



## Running tests

In order to run the unit tests stored under ```tests```, ```pytest``` can be used. To do so, navigate to ```tests``` 
folder and run the following command ```pytest -vv```.
Unit tests are made to test the functionality of some methods within the different modules and are not testing the 
mapping functionality.

## Contributors

[![Ghaith Arfaoui](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0001-9554-5684)
[Ghaith Arfaoui](https://orcid.org/0000-0001-9554-5684)

[![Maroua Jaoua](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0001-8109-9644) 
[Maroua Jaoua](https://orcid.org/0000-0001-8109-9644)



# License

[MIT License](https://github.com/GhaithArf/ro-crate-rda-madmp-mapper/blob/master/LICENSE)

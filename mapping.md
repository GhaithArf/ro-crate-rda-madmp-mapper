## Assumptions
<p>
  DMPs can include multiple datasets. However, ro-crate include only one
  dataset. The dataset can include other nested datasets. It is assumed that the
  data for the dataset at the root is equivalent to the data of DMP. Nested
  datasets will be included as elements of distributions.
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

## Mapped Properties

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
      <td valign="top">name</td>
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
      <td valign="top">value</td>
      <td valign="top">cost</td>
      <td valign="top">value</td>
      <td valign="top">cost</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">description</td>
      <td valign="top">Dataset</td>
      <td valign="top">description</td>
      <td valign="top">dmp</td>
      <td valign="top">
        It is assumed that the description of the DMP is the same as the
        desciption of the ro-crate.
      </td>
    </tr>
    <tr>
      <td valign="top">identifier</td>
      <td valign="top">Dataset</td>
      <td valign="top">identifier</td>
      <td valign="top">dmp_id</td>
      <td valign="top">
        It is assumed that the identifier of the dataset in ro-crate is the
        identifier of DMP. This is not always safe. The user is advised to
        create an identifier for the DMP as it is a broader concept.
      </td>
    </tr>
    <tr>
      <td valign="top">Language</td>
      <td valign="top">Dataset</td>
      <td valign="top">language</td>
      <td valign="top">dmp</td>
      <td valign="top"></td>
    </tr>
    <tr>
      <td valign="top">name</td>
      <td valign="top">Dataset</td>
      <td valign="top">title</td>
      <td valign="top">dmp</td>
      <td valign="top"></td>
    </tr>
  </tbody>
</table>

## Unmapped Properties of RDA DMP
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
      <td valign="top">contact_id, contributor_id, dmp_id</td>
      <td valign="top">
        For these attributes, there isn't an equivalent attribute. But, their
        children have equivalent attributes.
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
        ethical_issues_description, ethical_issues_exist, ethical_issues_report
      </td>
      <td valign="top">
        Equivalents to these attributes were not found in
        https://w3id.org/ro/crate/1.0/context.
      </td>
    </tr>
  </tbody>
</table>

## Unmapped Properties of ro-crate

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
  </tbody>
</table>

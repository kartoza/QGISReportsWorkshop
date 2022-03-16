from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')
def serial_var(variable, feature, parent):
    """
    Increments, sets and then returns the value of a project variable.
    <h2>Example usage:</h2>
    <ul>
      <li>serial_var('my_variable') -> 13</li>
    </ul>
    <p>Value of my_variable before calling the function: 12</p>
    <p>Value of my_variable after calling the function: 13</p>
    """
    project = QgsProject.instance()
    value = 0
    try:
        value = int(QgsExpressionContextUtils.projectScope(
            project).variable(variable))
        if value is None:
            value = 0
    except:
      pass
    value += 1
    QgsExpressionContextUtils.setProjectVariable(
        QgsProject.instance(), variable, value)

    return value

@qgsfunction(args='auto', group='Custom')
def reset_serial_var(variable, feature, parent):
    """
    Resets and the value of a project variable to zero.
    <h2>Example usage:</h2>
    <ul>
      <li>reset_serial_var('my_variable') -> None</li>
    </ul>
    <p>Value of my_variable before calling the function: 12</p>
    <p>Value of my_variable after calling the function: 0</p>
    """
    project = QgsProject.instance()
    QgsExpressionContextUtils.setProjectVariable(
        QgsProject.instance(), variable, 0)
    return None

@qgsfunction(args='auto', group='Custom')
def add_contents_entry(section, page_variable, feature, parent):
    """
    Adds a new row to the table of contents table.
<p>
    The table should be called 'report_contents' and be 
    structured with a 'section' and a 'page' column. No
    detailed checks are made to confirm this structure is
    in place.
</p><p>
    The page will be taken from the designated project
    variable as defined by the parameter 'page_variable'-
</p>

    <h2>Example usage:</h2>
    <ul>
      <li>add_contents_entry('Section 1','page_counter')</li>
    </ul>

<p>
    Returns None.
</p>

    """
    project = QgsProject.instance()
    page = 0
    try:
        page = int(QgsExpressionContextUtils.projectScope(
            project).variable(page_variable))
        if page is None:
            page = 0
    except:
      pass

    layer=None
    layers = QgsProject.instance().mapLayersByName('report_contents')
    if layers: 
      layer = layers[0]
    else:
      return None

    feature = QgsFeature(layer.fields())
    feature.setAttribute('section', section)
    feature.setAttribute('page', page)
    layer.dataProvider().addFeatures([feature])

@qgsfunction(args='auto', group='Custom')
def clear_contents_table(feature, parent):
    """
    Clears all the table of contents table's rows.
    <p>
        The table should be called 'report_contents'. No
        detailed checks are made to confirm table exists,
        is editable etc.
    </p>

        <h2>Example usage:</h2>
        <ul>
          <li>clear_contents_table()</li>
        </ul>

    <p>
        Returns None.
    </p>

    """
    layer=None
    layers = QgsProject.instance().mapLayersByName('report_contents')
    if layers: 
      layer = layers[0]
    else:
      return None
    with edit(layer):
        listOfIds = [feat.id() for feat in layer.getFeatures()]
        layer.deleteFeatures( listOfIds )
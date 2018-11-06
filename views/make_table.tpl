%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p><h3>Your TODO Items:</h3></p>
<table border="1">
%for key, value in dic.items():
  %id, title = key, value
  <tr>
  %for col in dic:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
<p>Show <a href="/done">Done Items</a></p>

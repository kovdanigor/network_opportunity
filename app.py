
import networkx as nx
from ipysigma import Sigma
from shinyswatch import theme
from shiny import reactive, req
from shiny.express import input, ui, render, session
from shinywidgets import render_widget, render_plotly
import pandas as pd
import netfunction
import plotly.express as px
from faicons import icon_svg
import plotly.graph_objects as go


















html_code = """
<style>
  /* Стили для модального окна */
  .modal_image {
      display: none; /* Скрыто по умолчанию */
      position: fixed;
      z-index: 1000; /* Располагается поверх всего */
      padding-top: 60px;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.9); /* Полупрозрачный фон */
  }
  .modal_image img {
      margin: auto;
      display: block;
      width: auto;
      height: auto;
      border: 1px solid black; /* Тонкая чёрная рамка для модального изображения */
  }
  
  /* Стили для миниатюр изображений на странице */
  .instruction-image {
      cursor: pointer;
      width: 90%;           /* Уменьшенный размер */
      max-width: 350px;     /* Ограничение максимальной ширины */
      border: 1px solid black;  /* Тонкая чёрная рамка */
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: block;
      margin: auto;
  }
</style>

<div style="max-width: 1200px; margin: auto; font-family: Arial, sans-serif;">

  <h3 style="text-align: center; margin-top: 20px;">Инструкция по загрузке и фильтрации данных</h3>
  <p style="text-align: center; margin-bottom: 40px;">Пошаговое руководство по загрузке и фильтрации данных в приложении</p>

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="http://tiny.cc/4j5n001" alt="Загрузка данных" onclick="openModal(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 1: Загрузка данных</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>На боковой панели найдите раздел <strong>"Обработка данных"</strong>.</li>
        <li>Нажмите кнопку <strong>"Обзор"</strong> и выберите Excel‑файл с данными о вакансиях, выгруженными из раздела <strong>"Данные"</strong> в личном кабинете аналитической платформы <a href="https://rosnavyk.ru/" target="_blank" rel="noopener noreferrer">РосНавык</a>.</li>
      </ol>
      <p><strong>Результат:</strong><br>
      После загрузки файла обновляются фильтры и аналитические панели.
      </p>
    </div>
  </div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
  <div style="flex: 1; padding: 10px;">
    <img class="instruction-image" src="http://tiny.cc/bd7n001" alt="Фильтрация данных" onclick="openModal(this.src)">
  </div>
  <div style="width: 1.5px; background-color: #333;"></div>
  <div style="flex: 1; padding: 10px;">
    <h5>Шаг 2: Фильтрация загруженных данных</h5>
    <p><strong>Действия:</strong></p>
    <ol>
      <li>Нажмите на секцию <strong>"Фильтрация загруженных данных"</strong>, чтобы развернуть список доступных фильтров.</li>
      <li>В зависимости от столбцов, присутствующих в загруженных данных, выберите подходящие фильтры.</li>
      <li>Используйте опцию мульти‑выбора для целевой фильтрации данных.</li>
    </ol>
    <p><strong>Результат:</strong><br>
    После настройки фильтров автоматически обновятся аналитические панели <strong>"Сеть"</strong> и <strong>"Рекомендация"</strong>.
    </p>
  </div>
</div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
  <div style="flex: 1; padding: 10px;">
    <img class="instruction-image" src="http://tiny.cc/ls6n001" alt="Фильтрация двумодального графа" onclick="openModal(this.src)">
  </div>
  <div style="width: 1.5px; background-color: #333;"></div>
  <div style="flex: 1; padding: 10px;">
    <h5>Шаг 3: Фильтрация двумодального графа</h5>
    <p><strong>Действия:</strong></p>
    <ol>
      <li>Нажмите на секцию <strong>"Фильтрация двумодального графа"</strong>, чтобы развернуть список доступных переменных.</li>
      <li>Выберите требуемые переменные для построения графа, демонстрирующего взаимосвязь двух категорий.</li>
      <li>Для просмотра графа выберите панель <strong>"Сеть"</strong> и перейдите в раздел <strong>"Двумодальный граф"</strong>.</li>
    </ol>
    <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
  <strong>Примечание:</strong><br>
  Двумодальный граф — это визуальное представление взаимосвязей между двумя разными категориями, например, работодателями и навыками, которые они требуют.<br>
  Эти графы позволяют анализировать спрос на навыки и профессии, выявлять возможности для партнерств, разрабатывать новые продукты и сервисы.</p>
  </div>
</div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="http://tiny.cc/ps6n001" alt="Граф со-встречаемости" onclick="openModal(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
    <h5>Шаг 4: Фильтрация графа со-встречаемости</h5>
    <p><strong>Действия:</strong></p>
    <ol>
        <li>Нажмите на секцию <strong>"Фильтрация графа со-встречаемости"</strong>, чтобы развернуть список доступных переменных.</li>
        <li>Выберите переменную для построения графа, который покажет, как часто одни и те же навыки встречаются в вакансиях.</li>
        <li>Для просмотра графа выберите панель <strong>"Сеть"</strong> и перейдите в раздел <strong>"Граф со-встречаемости"</strong>.</li>
    </ol>
    <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Граф со-встречаемости — это визуальное представление того, как часто встречаются одни и те же элементы, например, навыки в вакансиях.<br>
        Такой граф помогает выявить востребованные комбинации навыков, что может быть полезно для оптимизации образовательных программ и разработки новых продуктов или сервисов.
    </p>
    </div>

  </div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="http://tiny.cc/qs6n001" alt="Граф схожести" onclick="openModal(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 5: Фильтрация графа схожести</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Перейдите в секцию <strong>"Фильтрация графа схожести"</strong>.</li>
        <li>Выберите переменную для построения графа и настройте связующие переменные для анализа сходства вакансий.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
      <strong>Примечание:</strong><br>
      Граф схожести — это визуальное представление, которое показывает, насколько близки объекты (например, работодатели, специальности, регионы) по своим характеристикам через общие связующие переменные (например, навыки).<br> 
      Такой граф позволяет выявить группы с одинаковыми требованиями к навыкам.
      </p>
    </div>
  </div>

</div>

<div id="myModal" class="modal_image" onclick="closeModal()">
  <span class="close" onclick="closeModal()">&times;</span>
  <img id="modalImg" class="modal-content">
</div>

<script>
  function openModal(src) {
      var modal = document.getElementById("myModal");
      var modalImg = document.getElementById("modalImg");
      modal.style.display = "block";
      modalImg.src = src;
  }
  function closeModal() {
      var modal = document.getElementById("myModal");
      modal.style.display = "none";
  }
</script>
"""


html_code_2 = """
<style>
  /* Стили для модального окна */
  .modal_image {
      display: none; /* Скрыто по умолчанию */
      position: fixed;
      z-index: 1000; /* Располагается поверх всего */
      padding-top: 60px;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.9); /* Полупрозрачный фон */
  }
  .modal_image img {
      margin: auto;
      display: block;
      width: auto;
      height: auto;
      border: 1px solid black; /* Тонкая чёрная рамка для модального изображения */
  }
  
  /* Стили для миниатюр изображений на странице */
  .instruction-image {
      cursor: pointer;
      width: 90%;           /* Уменьшенный размер */
      max-width: 350px;     /* Ограничение максимальной ширины */
      border: 1px solid black;  /* Тонкая чёрная рамка */
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: block;
      margin: auto;
  }
</style>

<div style="max-width: 1200px; margin: auto; font-family: Arial, sans-serif;">

  <h3 style="text-align: center; margin-top: 20px;">Инструкция по работе с двумодальным графом</h3>
  <p style="text-align: center; margin-bottom: 40px;">Пошаговое руководство по работе с визуализацией двумодального графа</p>

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="http://tiny.cc/7rcn001" alt="Выбор переменных" onclick="openModal_bg(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 1: Выбор переменных</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Откройте секцию <strong>"Фильтрация двумодального графа"</strong> на боковой панели.</li>
        <li>Выберите переменные, определяющие взаимосвязи между категориями (например, специальности и навыки).</li>
        <li>Перейдите на панель <strong>"Сеть"</strong> и выберите раздел <strong>"Двумодальный граф"</strong> для просмотра визуализации.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Выбор переменных задаёт основу для построения графа, определяя, какие данные будут сопоставлены друг с другом.
      </p>
    </div>
  </div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="http://tiny.cc/orcn001" alt="Фильтры" onclick="openModal_bg(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 2: Общие фильтры</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>
          Используйте ползунок <strong>"Порог силы связей"</strong> для задания минимальной величины связи между узлами. Это помогает исключить слабые взаимосвязи.
        </li>
        <li>
          Настройте диапазоны для размеров узлов и ребер, чтобы задать визуальные свойства графа.
        </li>
        <li>
          Задайте значение <strong>"Разрешение Louvain"</strong> для разделения узлов на сообщества.
        </li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Фильтры контролируют базовые параметры графа: отсекают слабые связи, задают размеры узлов/ребер и помогают выявить структуру сообществ в сети.
      </p>
    </div>
  </div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-50.userapi.com/impg/ndM2vY1VKiEN8wr_meVURBpRvAHj6yxC6M1b0w/WDnrnqZXzNc.jpg?size=400x224&quality=95&sign=fba8fac350a40626d66ce7ee83bba94b&type=album" alt="Выделение цвета узла" onclick="openModal_bg(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 3: Выделение цвета узла</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Выберите опцию <strong>"Выделение цвета узла"</strong> в панели фильтров.</li>
        <li>Определите критерий окраски:
          <ul>
            <li><em>Модулярность</em> – узлы окрашиваются в зависимости от принадлежности к сетевым сообществам.</li>
            <li><em>Модальность</em> – одна категория узлов выделяется одним цветом, а другая - другим (например, специальности - синем цветом, а навыки - красным).</li>
            <li><em>Уникальность/общность</em> – уникальные узлы из второй переменной (например, навыки) выделяются одним цветом, а общие – другим.</li>
          </ul>
        </li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Выбор цвета узла помогает визуально различать группы элементов.
      </p>
    </div>
  </div>

  <hr style="border-top: 1px solid #ccc; margin: 40px 0;">

  
  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-45.userapi.com/impg/fkd7OZ083fp0P8VrZfpzfPdff116XTtKvqQ0Gw/gP0Ox-1DBvs.jpg?size=414x232&quality=95&sign=48ee13fba297a7c5258ba36acd53aa57&type=album" alt="Метрика размера узла" onclick="openModal_bg(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 4: Метрика размера узла</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Выберите опцию <strong>"Метрика размера узла"</strong> для определения важности узлов в графе.</li>
        <li>Обратите внимание на предлагаемые опции:
          <ul>
            <li><em>Центральность по степени</em> – оценивает количество прямых связей узла.</li>
            <li><em>Центральность по близости</em> – измеряет, насколько узел расположен близко к другим.</li>
            <li><em>Центральность по посредничеству</em> – показывает роль узла как связующего элемента между разными группами.</li>
          </ul>
        </li>
        <li>Настройте диапазон размеров узлов с помощью ползунка для визуального отражения выбранной метрики.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Метрика размера узла определяет, насколько важен каждый элемент. Узлы с большим количеством связей или критической ролью в сети будут отображаться крупнее.
      </p>
    </div>
  </div>

</div>


<div id="myModal_bg" class="modal_image" onclick="closeModal_bg()">
  <span class="close" onclick="closeModal_bg()">&times;</span>
  <img id="modalImg_bg" class="modal-content">
</div>

<script>
  function openModal_bg(src) {
      var modal = document.getElementById("myModal_bg");
      var modalImg = document.getElementById("modalImg_bg");
      modal.style.display = "block";
      modalImg.src = src;
  }
  function closeModal_bg() {
      var modal = document.getElementById("myModal_bg");
      modal.style.display = "none";
  }
</script>

"""


html_code_3 = """
<style>
  /* Стили для модального окна */
  .modal_image {
      display: none; /* Скрыто по умолчанию */
      position: fixed;
      z-index: 1000; /* Располагается поверх всего */
      padding-top: 60px;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.9); /* Полупрозрачный фон */
  }
  .modal_image img {
      margin: auto;
      display: block;
      width: auto;
      height: auto;
      border: 1px solid black; /* Тонкая чёрная рамка для модального изображения */
  }
  
  /* Стили для миниатюр изображений на странице */
  .instruction-image {
      cursor: pointer;
      width: 90%;           /* Уменьшенный размер */
      max-width: 350px;     /* Ограничение максимальной ширины */
      border: 1px solid black;  /* Тонкая чёрная рамка */
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: block;
      margin: auto;
  }
</style>

<div style="max-width: 1200px; margin: auto; font-family: Arial, sans-serif;">

  <h3 style="text-align: center; margin-top: 20px;">Инструкция по работе с графом со-встречаемости</h3>
  <p style="text-align: center; margin-bottom: 40px;">Пошаговое руководство по работе с визуализацией графа со-встречаемости</p>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-49.userapi.com/s/v1/if2/RcrjQP01fdC2EJ-Xq9XbkAtH33VbvSrzv2yXMFahCpuwR9OfySIJvWbVipVVPQV1Js9_azWRkgVISwUm101fgRD6.jpg?quality=95&as=32x18,48x28,72x42,108x62,160x92,240x138,360x208,423x244&from=bu&u=KThGeB4PMsPpF7A5NVvIHTdQiV9br6ZYO4VAdz9bWc4&cs=423x244" alt="Выбор переменных" onclick="openModal_sn(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 1: Выбор переменных</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Откройте секцию <strong>"Фильтрация графа со‑встречаемости"</strong> на боковой панели.</li>
        <li>Выберите доступную переменную (например, ключевые навыки) для определения взаимосвязей между навыками.</li>
        <li>Перейдите на панель <strong>"Сеть"</strong> и выберите раздел <strong>"Граф со‑встречаемости"</strong> для просмотра визуализации.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Этот шаг задаёт основу для построения графа на основе частоты совместного появления навыков в вакансиях.
      </p>
    </div>
  </div>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://psv4.userapi.com/s/v1/d/CDAFzsuxp7HTZX3TDBfcxilzhXwN7irp0IcWIWnwmerJ8ehfI1Z4exlX_YA-EFAKpHQQvxOugpc4c2n1DsSvQtQ2GVklHM9P2cHCCXUQbV_6YZxtGnjTVA/Semanticheskie_seti.png" alt="Общие фильтры" onclick="openModal_sn(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 2: Общие фильтры</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>
          Используйте ползунок <strong>"Порог силы связей"</strong> для задания минимальной величины связи между узлами. Это помогает исключить слабые взаимосвязи.
        </li>
        <li>
          Настройте диапазоны для размеров узлов и ребер, чтобы задать визуальные свойства графа.
        </li>
        <li>
          Задайте значение <strong>"Разрешение Louvain"</strong> для разделения узлов на сообщества.
        </li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Фильтры контролируют базовые параметры графа: отсекают слабые связи, задают размеры узлов/ребер и помогают выявить структуру сообществ в сети.
      </p>
    </div>
  </div>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-77.userapi.com/s/v1/if2/pa1Vb04rO0GiWY1-hBZt8zIKHuyT-i3QRw9G4hH47jXgbZf_lt62EKEz6ApqodqSgbWuEvaql_06hJQL9CSZsBt7.jpg?quality=95&as=32x17,48x26,72x39,108x58,160x86,240x129,360x194,413x222&from=bu&u=86EbK2FYdAOPSoeI6Xc_zXNxX_pd1XtzOS5DfX21Frc&cs=413x222" alt="Выделение цвета узла" onclick="openModal_sn(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>

    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 3: Выделение цвета узла</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Выберите опцию <strong>"Выделение цвета узла"</strong> в панели фильтров.</li>
        <li>Определите критерий окраски:
          <ul>
            <li><em>Модулярность</em> – узлы окрашиваются в зависимости от принадлежности к сетевым сообществам.</li>
            <li><em>Целевые узлы навыков</em> – узлы, соответствующие выбранным навыкам в секции <strong>"Фильтрация загруженных данных"</strong>, выделяются одним цветом, а остальные - другим.</li>
            <li><em>Заработная плата</em> – узлы окрашиваются градиентом (от светло-зелёного до тёмно-зелёного) в зависимости от медианного уровня зарплаты.</li>
          </ul>
        </li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Выбор цвета узла помогает визуально различать группы элементов.
      </p>
    </div>
  </div>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-45.userapi.com/impg/fkd7OZ083fp0P8VrZfpzfPdff116XTtKvqQ0Gw/gP0Ox-1DBvs.jpg?size=414x232&quality=95&sign=48ee13fba297a7c5258ba36acd53aa57&type=album" alt="Метрика размера узла" onclick="openModal_sn(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 4: Метрика размера узла</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Выберите опцию <strong>"Метрика размера узла"</strong> для определения важности узлов в графе.</li>
        <li>Обратите внимание на предлагаемые опции:
          <ul>
            <li><em>Центральность по степени</em> – оценивает количество прямых связей узла.</li>
            <li><em>Центральность по близости</em> – измеряет, насколько узел расположен близко к другим.</li>
            <li><em>Центральность по посредничеству</em> – показывает роль узла как связующего элемента между разными группами.</li>
          </ul>
        </li>
        <li>Настройте диапазон размеров узлов с помощью ползунка для визуального отражения выбранной метрики.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Метрика размера узла определяет, насколько важен каждый элемент. Узлы с большим количеством связей или критической ролью в сети будут отображаться крупнее.
      </p>
    </div>
  </div>
</div>

<div id="myModal_sn" class="modal_image" onclick="closeModal_sn()">
  <span class="close" onclick="closeModal_sn()">&times;</span>
  <img id="modalImg_sn" class="modal-content">
</div>

<script>
  function openModal_sn(src) {
      var modal = document.getElementById("myModal_sn");
      var modalImg = document.getElementById("modalImg_sn");
      modal.style.display = "block";
      modalImg.src = src;
  }
  function closeModal_sn() {
      var modal = document.getElementById("myModal_sn");
      modal.style.display = "none";
  }
</script>

"""



html_code_4 = """
<style>
  /* Стили для модального окна */
  .modal_image {
      display: none; /* Скрыто по умолчанию */
      position: fixed;
      z-index: 1000; /* Располагается поверх всего */
      padding-top: 60px;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.9); /* Полупрозрачный фон */
  }
  .modal_image img {
      margin: auto;
      display: block;
      width: auto;
      height: auto;
      border: 1px solid black; /* Тонкая чёрная рамка для модального изображения */
  }
  
  /* Стили для миниатюр изображений на странице */
  .instruction-image {
      cursor: pointer;
      width: 90%;           /* Уменьшенный размер */
      max-width: 350px;     /* Ограничение максимальной ширины */
      border: 1px solid black;  /* Тонкая чёрная рамка */
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: block;
      margin: auto;
  }
</style>

<div style="max-width: 1200px; margin: auto; font-family: Arial, sans-serif;">

  <h3 style="text-align: center; margin-top: 20px;">Инструкция по работе с графом схожести</h3>
  <p style="text-align: center; margin-bottom: 40px;">Пошаговое руководство по работе с визуализацией графа схожести</p>



  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-79.userapi.com/s/v1/if2/Ibhlwtx9-hW9uvA-mzR07MJZekXQAsiEycrNUNFtyJ3boEdG8Plpvg_a2oYcHFBf8danJZw-n77pU76w4_fOpn5M.jpg?quality=95&as=32x26,48x40,72x59,108x89,160x132,240x198,360x296,425x350&from=bu&u=u8dEBtFB6HwleXA0cYy-Zp5FLHfmOWnKzLil6gjROok&cs=425x350" alt="Выбор переменных" onclick="openModal_sim(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 1: Выбор переменных</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Откройте секцию <strong>"Фильтрация графа схожести"</strong> на боковой панели.</li>
        <li>Выберите необходимые переменные (например, работодатели и навыки) для определения схожести объектов.</li>
        <li>Перейдите на вкладку <strong>"Сеть"</strong> и выберите раздел <strong>"Граф схожести"</strong> для просмотра визуализации.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Выбор переменных задаёт основу для анализа схожести между объектами, определяя, какие данные будут сравниваться.
      </p>
    </div>
  </div>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://psv4.userapi.com/s/v1/d/BqFklNds257A6p-yqyNlOOfEtiRhhRqSnQQjVsbiK7K_rppgFGzJB81DZhE-fUUJ3fjKKL5ly3u4XClWQ8RkAERxz4_MU7r_r1pH3ygiOzxCAt_RJ6wR5A/Graf_skhozhesti.png" alt="Общие фильтры" onclick="openModal_sim(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 2: Общие фильтры</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>
          Используйте ползунок <strong>"Порог схожести"</strong> для задания минимального уровня схожести между объектами. Значение устанавливается от 0 до 100%.
        </li>
        <li>
          Настройте диапазоны для размера узлов и ребер с помощью соответствующих ползунков.
        </li>
        <li>
          Задайте параметр <strong>"Разрешение Louvain"</strong> для более детального выделения сообществ в графе.
        </li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Общие фильтры управляют базовыми параметрами графа, исключая слабые связи и задавая визуальные пределы для узлов и ребер.
      </p>
    </div>
  </div>
</div>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-72.userapi.com/s/v1/if2/0kZWQSG-8TMowzSBJSt90CjS1YewERfHLegHrRWe0JDh-RuDz9P-ENWfwev0VoJiMnMBYJfW42hfeN1qotbvsHhZ.jpg?quality=95&as=32x16,48x25,72x37,108x55,160x82,240x123,360x184,410x210&from=bu&u=kXXyGHF1Q13ihhxpXv0BQHWVnfFHDUxIPfUCx25blHM&cs=410x210" alt="Выделение цвета узла" onclick="openModal_sim(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 3: Выделение цвета узла</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Выберите опцию <strong>"Выделение цвета узла"</strong> в панели фильтров.</li>
        <li>Определите способ окраски:
          <ul>
            <li><em>Модулярность</em> – узлы окрашиваются в зависимости от принадлежности к сетевым сообществам.</li>
            <li><em>Заработная плата</em> – узлы окрашиваются градиентом (от светло-зелёного до тёмно-зелёного) в зависимости от медианного уровня зарплаты.</li>
          </ul>
        </li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Выбор цвета узла помогает визуально различать группы элементов.
      </p>
    </div>
  </div>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://sun9-45.userapi.com/impg/fkd7OZ083fp0P8VrZfpzfPdff116XTtKvqQ0Gw/gP0Ox-1DBvs.jpg?size=414x232&quality=95&sign=48ee13fba297a7c5258ba36acd53aa57&type=album" alt="Метрика размера узла" onclick="openModal_sim(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
        <h5>Шаг 4: Метрика размера узла</h5>
        <p><strong>Действия:</strong></p>
        <ol>
          <li>Выберите опцию <strong>"Метрика размера узла"</strong> для определения важности узлов в графе.</li>
          <li>Обратите внимание на предлагаемые опции:
            <ul>
              <li><em>Центральность по степени</em> – оценивает количество прямых связей узла.</li>
              <li><em>Центральность по близости</em> – измеряет, насколько узел расположен близко к другим.</li>
              <li><em>Центральность по посредничеству</em> – показывает роль узла как связующего элемента между разными группами.</li>
            </ul>
          </li>
          <li>Настройте диапазон размеров узлов с помощью ползунка для визуального отражения выбранной метрики.</li>
        </ol>
        <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
          <strong>Примечание:</strong><br>
          Метрика размера узла определяет, насколько важен каждый элемент. Узлы с большим количеством связей или критической ролью в сети будут отображаться крупнее.
        </p>
      </div>
  </div>

<div id="myModal_sim" class="modal_image" onclick="closeModal_sim()">
  <span class="close" onclick="closeModal_sim()">&times;</span>
  <img id="modalImg_sim" class="modal-content">
</div>

<script>
  function openModal_sim(src) {
      var modal = document.getElementById("myModal_sim");
      var modalImg = document.getElementById("modalImg_sim");
      modal.style.display = "block";
      modalImg.src = src;
  }
  function closeModal_sim() {
      var modal = document.getElementById("myModal_sim");
      modal.style.display = "none";
  }
</script>


"""


html_code_5 = """

<style>
  /* Стили для модального окна */
  .modal_image {
      display: none; /* Скрыто по умолчанию */
      position: fixed;
      z-index: 1000; /* Располагается поверх всего */
      padding-top: 60px;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.9); /* Полупрозрачный фон */
  }
  .modal_image img {
      margin: auto;
      display: block;
      width: auto;
      height: auto;
      border: 1px solid black; /* Тонкая чёрная рамка для модального изображения */
  }
  
  /* Стили для миниатюр изображений на странице */
  .instruction-image {
      cursor: pointer;
      width: 90%;           /* Уменьшенный размер */
      max-width: 400px;     /* Ограничение максимальной ширины */
      border: 1px solid black;  /* Тонкая чёрная рамка */
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: block;
      margin: auto;
  }
</style>

<div style="max-width: 1200px; margin: auto; font-family: Arial, sans-serif;">

  <h3 style="text-align: center; margin-top: 20px;">Инструкция по работе с панелью "Рекомендация"</h3>
  <p style="text-align: center; margin-bottom: 40px;">Пошаговое руководство по работе с визуализацией рекомендаций</p>


  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="http://tiny.cc/7rcn001" alt="Выбор переменных" onclick="openModal_bg(this.src)">
    </div>
    <div style="width: 1.5px; background-color: #333;"></div>
    <div style="flex: 1; padding: 10px;">
      <h5>Шаг 1: Выбор переменных</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Откройте секцию <strong>"Фильтрация двумодального графа"</strong> на боковой панели.</li>
        <li>Выберите переменные, определяющие взаимосвязи между категориями (например, специальности и навыки).</li>
        <li>Двумодальные графы используются для рекомендации схожих и соседних узлов.</li>
      </ol>
    </div>
  </div>



  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://psv4.userapi.com/s/v1/d/NFSjWOfys0efVpveTMwooXuYXZxYz7scKvnIe7VR_dXfFxK2V1a8gff5mbXJJz4jlJLlITXFkHv7G8BSp-urrYIajTaDUJq-7EqCDP0gM2M_Xy-6K-rBrw/Rekomendatsia_skhozhikh_uzlov.png" alt="Выбор узла (схожие узлы)" onclick="openModal_rs(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Рекомендация схожих узлов</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Перейдите на вкладку <strong>"Рекомендация"</strong> и выберите раздел <strong>"Рекомендация схожих узлов"</strong> для просмотра визуализации.</li>
        <li>Выберите интересующий вас узел (например, специальность или навык) из выпадающего списка.</li>
        <li>Укажите количество рекомендуемых узлов в поле <strong>"Количество наблюдений"</strong>.</li>
        <li>Система рассчитает схожесть выбранного узла с другими на основе весовых характеристик их связей и отобразит столбчатую диаграмму с результатами.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Столбчатая диаграмма иллюстрирует процентное соотношение схожести между узлами, позволяя выявить наиболее похожие объекты внутри графа.
      </p>
    </div>
  </div>

  <div style="display: flex; margin-bottom: 40px; align-items: stretch;">
    
    <div style="flex: 1; padding: 10px;">
      <img class="instruction-image" src="https://psv4.userapi.com/s/v1/d/MzPjAYLZXjgLBxIMM_iTTzErci8SD2vjDY4pmUiyHOpeY_avb0KYkPCc3YS_9m_g4QGmohKq8z7iK6M2qHb60UAWtgDhVeVliTSZd7aZ9lMpvCazU6zojw/Rekomendatsia_sosednikh_uzlov.png" alt="Выбор узла (соседние узлы)" onclick="openModal_rs(this.src)">
    </div>
    
    <div style="width: 1.5px; background-color: #333;"></div>
    
    <div style="flex: 1; padding: 10px;">
      <h5>Рекомендация соседних узлов</h5>
      <p><strong>Действия:</strong></p>
      <ol>
        <li>Перейдите на вкладку <strong>"Рекомендация"</strong> и выберите раздел <strong>"Рекомендация соседних узлов"</strong> для просмотра визуализации.</li>
        <li>Выберите из списка узел, для которого необходимо найти непосредственно связанные соседние узлы.</li>
        <li>Укажите количество рекомендуемых соседних узлов через поле <strong>"Количество наблюдений"</strong>.</li>
        <li>Система сформирует столбчатую диаграмму, отображающую вес (интенсивность связи) между выбранным узлом и его ближайшими соседями.</li>
      </ol>
      <p style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; padding: 10px; font-size: 14px; line-height: 1.5;">
        <strong>Примечание:</strong><br>
        Отображается информация о сильнейших связях выбранного узла, что помогает выявить его ключевых соседей в графе
      </p>
    </div>
  </div>
</div>


<div style="background-color: #f7f7f7; border-left: 4px solid #fbe1e0; margin: 20px 0; padding: 10px; font-size: 14px; line-height: 1.5;">
  <strong>Логика рекомендаций:</strong><br>
  Рекомендации рассчитываются на основе анализа взаимосвязей в графе с применением обобщённого коэффициента Жаккара. Этот коэффициент вычисляется путем сравнения двух векторов, представляющих весовые характеристики связей выбранного узла и другого узла. Он определяется как отношение суммы минимальных значений к сумме максимальных, что дает значение от 0 до 1. Узлы с более высоким коэффициентом схожести (ближе к 1) рекомендуются как схожие.<br>
  Аналогично, при рекомендации соседних узлов система анализирует прямые связи и их весовые показатели, позволяя выделить ближайших и наиболее влиятельных соседей.
</div>


<div id="myModal_rs" class="modal_image" onclick="closeModal_rs()">
  <span class="close" onclick="closeModal_rs()">&times;</span>
  <img id="modalImg_rs" class="modal-content">
</div>

<script>
  function openModal_rs(src) {
      var modal = document.getElementById("myModal_rs");
      var modalImg = document.getElementById("modalImg_rs");
      modal.style.display = "block";
      modalImg.src = src;
  }
  function closeModal_rs() {
      var modal = document.getElementById("myModal_rs");
      modal.style.display = "none";
  }
</script>

"""


# Настройки страницы
ui.page_opts(
    title=ui.div(
        icon_svg("vector-square"),      # Иконка сети из faicons
        "Networks of Opportunity",
        style="display: flex; align-items: center;"
    ),
    fillable=True,
    id="page",
    theme=theme.journal
)



# Sidebar: Обработка данных и универсальные фильтры для графов
with ui.sidebar(width=400):
    # Обработка данных
    ui.HTML("<h5> ⚙️Обработка данных</h5>")
    ui.hr()

    with ui.card(full_screen=False):
        ui.input_file("file", "Загрузить данные:", accept=".xlsx", width='400px',
                      button_label='Обзор', placeholder='Файл отсутствует')

    # Универсальные фильтры для сетей
    with ui.card(full_screen=False):
        with ui.accordion(id="acc", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация загруженных данных', value='filter_panel'):
                ui.input_date_range(
                    "pub_date", "Дата публикации:",
                    start="2024-01-01", end="2024-12-31",
                    min="2024-01-01", max="2024-12-31", width='400px'
                )

                ui.input_selectize("specialty", "Название специальности:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("employer", "Работодатель:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("industry", "Отрасль деятельности:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("key_skills", "Ключевые навыки:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("hard_skills", "Профессиональные навыки:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("soft_skills", "Надпрофессиональные навыки:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("region", "Название региона:", choices=[],
                                   multiple=True, width=200)

                ui.input_selectize("employment_type", "Вид трудоустройства:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("experience", "Опыт работы:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("language_requirements", "Требования к знанию языков:",
                                   choices=[], multiple=True, width='400px')

                ui.input_selectize("for_minors", "Для несовершеннолетних:",
                                   choices=["Истина", "Ложь"], multiple=True, width='400px')

                ui.input_selectize("has_test_task", "Наличие тестового задания:",
                                   choices=["Истина", "Ложь"], multiple=True, width='400px')

                ui.input_selectize("for_disabled", "Для людей с ограниченными возможностями:",
                                   choices=["Истина", "Ложь"], multiple=True, width='400px')

                ui.input_slider("salary", "Заработная плата:", min=0,
                                max=100000, value=[0, 100000])
    ui.hr()

    with ui.card(full_screen=False):
        with ui.accordion(id="acc2", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация двумодального графа'):
                ui.input_selectize(
                    "bipartite_col", "Выбор первой переменной для графа:", choices=[], width='400px')
                ui.input_selectize(
                    "bipartite_row", "Выбор второй переменной для графа:", choices=[], width='400px')

    with ui.card(full_screen=False):
        with ui.accordion(id="acc3", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация графа со-встречаемости'):
                ui.input_selectize(
                    "onemode_semantic", "Выбор переменной для графа:", choices=[], width='400px')

    with ui.card(full_screen=False):
        with ui.accordion(id="acc4", multiple=True, open=False):
            with ui.accordion_panel('Фильтрация графа схожести'):
                ui.input_selectize(
                    "onemode_similarity", "Выбор переменной для графа:", choices=[], width='400px')

                ui.input_selectize(
                    "var_broker", "Связующая переменная:", choices=[], width='400px')

    ui.hr()


# Реактивные вычисления и эффекты


# @reactive.calc
# def df():
#     f = req(input.file())
#     return pd.read_excel(f[0]['datapath'])

@reactive.calc
def df():
    req(input.file())

    try:
        file_path = input.file()[0]['datapath']
        df = pd.read_excel(file_path)

        # # Проверка минимальных требований
        # required_cols = ['Работодатель', 'Ключевые навыки']
        # missing_cols = [col for col in required_cols if col not in df.columns]

        # if missing_cols:
        #     ui.notification_show(
        #         f"Файл не содержит обязательные колонки: {missing_cols}",
        #         type="error", duration=10
        #     )
        #     return pd.DataFrame()

        return df

    except Exception as e:
        ui.notification_show(
            f"Ошибка чтения файла: {str(e)}", type="error", duration=10)
        return pd.DataFrame()


@reactive.calc
def processed_data():
    data = df()

    try:
        for col in ['Работодатель', 'Ключевые навыки']:
            if col in data.columns:
                data = data.dropna(subset=[col])

        for col in ['Профессиональные навыки', 'Надпрофессиональные навыки', 'Ключевые навыки']:
            if col in data.columns:
                data[col] = data[col].apply(netfunction.parse_skills)

        if 'Дата публикации' in data.columns:
            data['Дата публикации'] = pd.to_datetime(
                data['Дата публикации'], errors='coerce')

        data.reset_index(inplace=True, drop=True)
        return data
    except Exception as e:
        ui.notification_show(
            f"Ошибка обработки данных: {str(e)}", type="error")
        return None

# --- Остальное


# @reactive.effect
# def update_selects():
#     row_val = input.bipartite_row()
#     col_val = input.bipartite_col()

#     new_row_choices = [r for r in row_choices if r != col_val]
#     if row_val not in new_row_choices:
#         row_val = new_row_choices[0] if new_row_choices else None

#     new_col_choices = [c for c in col_choices if c != row_val]
#     if col_val not in new_col_choices:
#         col_val = new_col_choices[0] if new_col_choices else None

#     ui.update_selectize(
#         "bipartite_row", choices=new_row_choices, selected=row_val)
#     ui.update_selectize(
#         "bipartite_col", choices=new_col_choices, selected=col_val)

@reactive.effect
@reactive.event(input.file)
def remove_missing_inputs():
    df = processed_data()
    df_columns = df.columns.tolist()

    # Маппинг: ключ — имя инпута, значение — ожидаемый столбец
    inputs_and_columns = {
        "pub_date": "Дата публикации",
        "specialty": "Название специальности",
        "employer": "Работодатель",
        "industry": "Отрасль деятельности",
        "key_skills": "Ключевые навыки",
        "hard_skills": "Профессиональные навыки",
        "soft_skills": "Надпрофессиональные навыки",
        "region": "Название региона",
        "employment_type": "Вид трудоустройства",
        "experience": "Опыт работы",
        "salary": "Заработная плата",
        "language_requirements": "Требования к знанию языков",
        "for_minors": "Для несовершеннолетних",
        "has_test_task": "Наличие тестового задания",
        "for_disabled": "Для людей с ограниченными возможностями"
    }

    for input_id, column_name in inputs_and_columns.items():
        if column_name not in df_columns or df[column_name].dropna().empty:
            ui.remove_ui(f"div.form-group:has(#{input_id})")
        # if input.language_requirements() == False:
        #    ui.remove_ui(f"div.form-group:has(#language_requirements)")

# Попытки обновления:

@reactive.effect
def _():
    df = processed_data()
    df_columns = df.columns.tolist()

    # Маппинг: ключ — имя инпута, значение — ожидаемый столбец
    inputs_and_columns = {
        "pub_date": "Дата публикации",
        "specialty": "Название специальности",
        "employer": "Работодатель",
        "industry": "Отрасль деятельности",
        "key_skills": "Ключевые навыки",
        "hard_skills": "Профессиональные навыки",
        "soft_skills": "Надпрофессиональные навыки",
        "region": "Название региона",
        "employment_type": "Вид трудоустройства",
        "experience": "Опыт работы",
        "salary": "Заработная плата",
        "language_requirements": "Требования к знанию языков",
        "for_minors": "Для несовершеннолетних",
        "has_test_task": "Наличие тестового задания",
        "for_disabled": "Для людей с ограниченными возможностями"
    }

    if 'Профессиональные навыки' in df_columns:
        ui.insert_ui(
        ui.input_selectize("hard_skills", "Профессиональные навыки:",
                           choices=[], multiple=True, width='400px'),
        selector="div.form-group:has(#filter_panel)",
        where="beforeEnd",
        )



@reactive.effect
def update_all_selects():
    df = processed_data()
    available_cols = df.columns.tolist()

    # ======= Двумодальный граф =======
    col_choices = [col for col in ['Название специальности',
                                   'Работодатель', 'Название региона'] if col in available_cols]
    row_choices = [row for row in ['Ключевые навыки', 'Название специальности', 'Работодатель', 'Название региона',
                                   'Профессиональные навыки', 'Надпрофессиональные навыки'] if row in available_cols]

    row_val = input.bipartite_row()
    col_val = input.bipartite_col()

    # Обновлённые допустимые значения
    row_choices = [r for r in row_choices if r != col_val]
    if row_val not in row_choices:
        row_val = row_choices[0] if row_choices else None

    col_choices = [c for c in col_choices if c != row_val]
    if col_val not in col_choices:
        col_val = col_choices[0] if col_choices else None

    ui.update_selectize("bipartite_row", choices=row_choices, selected=row_val)
    ui.update_selectize("bipartite_col", choices=col_choices, selected=col_val)

    # ======= Со-встречаемость =======
    onemode_semantic_choices = [c for c in ['Ключевые навыки', 'Профессиональные навыки', 'Надпрофессиональные навыки']
                                if c in available_cols]
    current_onemode = input.onemode_semantic()
    if current_onemode not in onemode_semantic_choices:
        current_onemode = onemode_semantic_choices[0] if onemode_semantic_choices else None
    ui.update_selectize(
        "onemode_semantic", choices=onemode_semantic_choices, selected=current_onemode)

    # ======= Граф схожести =======
    sim_choices_1 = [c for c in ['Название специальности',
                                 'Работодатель', 'Название региона'] if c in available_cols]
    sim_choices_2 = [c for c in ['Ключевые навыки', 'Профессиональные навыки', 'Надпрофессиональные навыки']
                     if c in available_cols]

    sim_var = input.onemode_similarity()
    var_broker = input.var_broker()

    if sim_var not in sim_choices_1:
        sim_var = sim_choices_1[0] if sim_choices_1 else None

    if var_broker not in sim_choices_2:
        var_broker = sim_choices_2[0] if sim_choices_2 else None

    ui.update_selectize("onemode_similarity",
                        choices=sim_choices_1, selected=sim_var)
    ui.update_selectize("var_broker", choices=sim_choices_2,
                        selected=var_broker)


@reactive.effect
def update_filter_choices():
    data = processed_data()
    available_cols = data.columns.tolist()

    if "Опыт работы" in available_cols:
        exp_choices = sorted(data["Опыт работы"].dropna().unique().tolist())
        ui.update_selectize("experience", choices=exp_choices)

    if "Название региона" in available_cols:
        region_choices = sorted(
            data["Название региона"].dropna().unique().tolist())
        ui.update_selectize("region", choices=region_choices)

    if "Работодатель" in available_cols:
        employer_choices = sorted(
            data['Работодатель'].dropna().unique().tolist())
        ui.update_selectize("employer", choices=employer_choices)

    if "Название специальности" in available_cols:
        specialty_choices = sorted(
            data["Название специальности"].dropna().unique().tolist())
        ui.update_selectize("specialty", choices=specialty_choices)

    if "Вид трудоустройства" in available_cols:
        employment_choices = sorted(
            data["Вид трудоустройства"].dropna().unique().tolist())
        ui.update_selectize("employment_type", choices=employment_choices)

    if "Отрасль деятельности" in available_cols:
        industry_choices = sorted(data["Отрасль деятельности"].str.split(
            ';').explode().dropna().unique().tolist())
        ui.update_selectize("industry", choices=industry_choices)

    if "Ключевые навыки" in available_cols:
        skills_choices = sorted(
            data["Ключевые навыки"].explode().dropna().unique().tolist())
        ui.update_selectize("key_skills", choices=skills_choices)

    if "Профессиональные навыки" in available_cols:
        skills_choices = sorted(
            data["Профессиональные навыки"].explode().dropna().unique().tolist())
        ui.update_selectize("hard_skills", choices=skills_choices)

    if "Надпрофессиональные навыки" in available_cols:
        skills_choices = sorted(
            data["Надпрофессиональные навыки"].explode().dropna().unique().tolist())
        ui.update_selectize("soft_skills", choices=skills_choices)

    if "Требования к знанию языков" in available_cols:
        language_choices = sorted(
            data["Требования к знанию языков"].dropna().unique().tolist())
        ui.update_selectize("language_requirements", choices=language_choices)


# remove ui

@reactive.effect
def update_date_range():
    data = processed_data()
    if not data.empty and 'Дата публикации' in data.columns:
        dates = data['Дата публикации']
        min_date = dates.min().date().isoformat()
        max_date = dates.max().date().isoformat()
        ui.update_date_range("pub_date", min=min_date,
                             max=max_date, start=min_date, end=max_date)


@reactive.effect
def update_salary_range():
    data = processed_data()
    if not data.empty and 'Заработная плата' in data.columns:
        min_salary = int(data['Заработная плата'].min())
        max_salary = int(data['Заработная плата'].max())
        ui.update_slider("salary", min=min_salary,
                         max=max_salary, value=[min_salary, max_salary])


@reactive.calc
def filtered_data():
    data = processed_data()
    if input.pub_date() and 'Дата публикации' in data.columns:
        start_date, end_date = input.pub_date()
        data = data[(data['Дата публикации'] >= pd.to_datetime(start_date)) &
                    (data['Дата публикации'] <= pd.to_datetime(end_date))]

    if input.experience() and 'Опыт работы' in data.columns:
        data = data[data['Опыт работы'].isin(input.experience())]

    if input.region() and 'Название региона' in data.columns:
        data = data[data['Название региона'].isin(input.region())]

    if input.salary() and 'Заработная плата' in data.columns:
        min_salary, max_salary = input.salary()
        data = data[(data['Заработная плата'] >= min_salary) &
                    (data['Заработная плата'] <= max_salary)]

    if input.employer() and 'Работодатель' in data.columns:
        data = data[data['Работодатель'].isin(input.employer())]

    if input.specialty() and 'Название специальности' in data.columns:
        data = data[data['Название специальности'].isin(input.specialty())]

    if input.employment_type() and 'Вид трудоустройства' in data.columns:
        data = data[data['Вид трудоустройства'].isin(input.employment_type())]

    if input.industry() and 'Отрасль деятельности' in data.columns:
        pattern = '|'.join(input.industry())
        data = data[data['Отрасль деятельности'].str.contains(
            pattern, na=False)]

    if input.key_skills() and 'Ключевые навыки' in data.columns:
        pattern = '|'.join(input.key_skills())
        data['Обработанные навыки'] = data['Ключевые навыки'].apply(
            lambda x: ''.join(x))
        data = data[data['Обработанные навыки'].str.contains(pattern)]

    if input.hard_skills() and 'Профессиональные навыки' in data.columns:
        pattern = '|'.join(input.hard_skills())
        data['Обработанные профессиональные навыки'] = data['Профессиональные навыки'].apply(
            lambda x: ''.join(x))
        data = data[data['Обработанные профессиональные навыки'].str.contains(
            pattern)]

    if input.soft_skills() and 'Надпрофессиональные навыки' in data.columns:
        pattern = '|'.join(input.soft_skills())
        data['Обработанные надпрофессиональные навыки'] = data['Надпрофессиональные навыки'].apply(
            lambda x: ''.join(x))
        data = data[data['Обработанные надпрофессиональные навыки'].str.contains(
            pattern)]

    if input.language_requirements() and 'Требования к знанию языков' in data.columns:
        pattern = '|'.join(input.language_requirements())
        data = data[data['Требования к знанию языков'].str.contains(
            pattern, na=False)]

    if input.for_minors() and 'Для несовершеннолетних' in data.columns:
        selected = [True if x == 'Истина' else False if x ==
                    'Ложь' else None for x in input.for_minors()]
        data = data[data['Для несовершеннолетних'].isin(selected)]

    if input.has_test_task() and 'Наличие тестового задания' in data.columns:
        selected = [True if x == 'Истина' else False if x ==
                    'Ложь' else None for x in input.has_test_task()]
        data = data[data['Наличие тестового задания'].isin(selected)]

    if input.for_disabled() and 'Для людей с ограниченными возможностями' in data.columns:
        selected = [True if x == 'Истина' else False if x ==
                    'Ложь' else None for x in input.for_disabled()]
        data = data[data['Для людей с ограниченными возможностями'].isin(
            selected)]

    return data


@reactive.calc
def semantic_cooccurrence_matrix():
    data = filtered_data()
    if data.empty:
        return pd.DataFrame()
    try:
        return netfunction.create_co_occurrence_matrix(data, input.onemode_semantic())
    except:
        ui.notification_show("❌ Ошибка построения матрицы со-встречаемости",
                             type="error", duration=10)
        return pd.DataFrame()


@reactive.calc
def semantic_graph():
    matrix = semantic_cooccurrence_matrix()
    if matrix.empty:
        return None
    try:
        G = nx.from_pandas_adjacency(matrix)
        return G
    except:
        ui.notification_show("❌ Ошибка построения графа со-встречаемости",
                             type="error", duration=10)
        return pd.DataFrame()


@reactive.calc
def bipartite_matrix_custom():
    data = filtered_data()
    if data.empty:
        return pd.DataFrame()
    col_var = input.bipartite_col() or 'Название специальности'
    row_var = input.bipartite_row() or 'Название региона'
    return netfunction.create_group_values_matrix(data, col_var, row_var)


@reactive.calc
def bipartite_graph():
    matrix = bipartite_matrix_custom()
    if matrix.empty:
        return None
    return netfunction.create_bipartite_graph(matrix)


#  Одномодальный схожесть

@reactive.calc
def similarity_bipartite_matrix():
    data = filtered_data()
    if data.empty:
        return pd.DataFrame()
    return netfunction.create_group_values_matrix(data,
                                                  input.onemode_similarity(),
                                                  input.var_broker())


@reactive.calc
def similarity_graph():
    matrix = similarity_bipartite_matrix()
    matrix = netfunction.create_unimodal_matrix(matrix)
    if matrix.empty:
        return None
    try:
        G = nx.from_pandas_adjacency(matrix)
        return G
    except:
        ui.notification_show("❌ Ошибка создания одномодального графа схожести",
                             type="error", duration=10)
        return pd.DataFrame()


# --- Панели ---

ui.nav_spacer()

with ui.nav_panel('О проекте', icon=icon_svg("circle-info")):
    with ui.card(full_screen=True):
        ui.HTML(
            """
    <div>
       <h3>Основная суть проекта </h3>
       <p>
         <strong>Networks of Opportunity</strong> — это интерактивное веб-приложение для анализа данных о вакансиях, собранных в рамках проекта 
         <a href="https://rosnavyk.ru/" target="_blank" rel="noopener noreferrer">РосНавык</a>.
       </p>
       <h4>Функционал приложения</h4>
       <ul>
         <li><strong>Визуализировать связи</strong> 🔗 между навыками, специальностями, регионами, работодателями и другими переменными через двумодальные и одномодальные графы.</li>
         <li><strong>Анализировать данные</strong> 📊 с помощью фильтров (работодатель, навыки, заработная плата, опыт работы и др.).</li>
         <li><strong>Искать схожие узлы в графе</strong> 🔍 через векторное сходство.</li>
         <li><strong>Определять целевые навыки</strong> 🎯, необходимые для получения сразу нескольких квалификаций.</li>
         <li><strong>Анализировать кластеры компетенций</strong> 🧠 с помощью выделения сообществ в графе.</li>
         <li><strong>Оценивать ценность навыков</strong> 💰 через привязку к зарплатным предложениям.</li>
       </ul>
       <hr>
       <h4>Как можно использовать веб-приложение для анализа рынка труда и компетенций 🌐</h4>
       <ul>
         <li><strong>Выявлять</strong>, какие навыки чаще всего требуются совместно в вакансиях, чтобы строить актуальные профили компетенций для разных специальностей.</li>
         <li><strong>Определять</strong> пересекающиеся навыки между различными специальностями, чтобы находить универсальные и смежные компетенции для переквалификации или расширения профиля кандидата.</li>
         <li><strong>Находить</strong> группы похожих между собой специальностей по требуемым навыкам для планирования карьерных переходов и построения альтернативных карьерных траекторий.</li>
         <li><strong>Анализировать спрос</strong> на навыки и профессии со стороны компаний, чтобы выявлять возможности для партнерств, стажировок или усиления кадровой политики.</li>
         <li><strong>Разрабатывать</strong> новые продукты и сервисы в области образования, HR или рекрутинга на основе анализа текущего рынка требований к навыкам.</li>
         <li><strong>Фокусироваться</strong> на дорогостоящих и актуальных для топ-компаний навыках для создания коммерчески успешных программ и проектов.</li>
       </ul>
       <hr>
       <h4>Основные компоненты приложения</h4>
       <h5>1. Боковая панель 📑</h5>
       <ul>
         <li><strong>Загрузка данных</strong>: Загрузка Excel-файла с вакансиями.</li>
         <li>
           <strong>Фильтры данных</strong>:
           <ul>
             <li>Дата публикации, регион, заработная плата, опыт работы, специальность.</li>
             <li>Автоматическое обновление диапазонов фильтров на основе структуры загруженного датасета.</li>
           </ul>
         </li>
         <li><strong>Настройки графа</strong>: Выбор переменных для двумодального графа (например, "Специальность ↔ Навыки").</li>
         <li><strong>Порог фильтрации</strong> для графов по силе связей и настройка параметров визуализации (размер узлов, размер ребер, цветовая кодировка).</li>
       </ul>
       <h5>2. Основные панели для анализа данных 📚</h5>
       <ul>
         <li>
           <strong>Вкладка "Сеть"</strong>:
           <ul>
             <li><strong>Двумодальный граф</strong>: Визуализация связей между двумя категориями (например, "Работодатель ↔ Навыки").</li>
             <li><strong>Одномодальный граф</strong>: 
               <ul>
                 <li>Построение графа со-встречаемости по частоте совместного появления в вакансиях (например, "Навыки ↔ Навыки")</li>
                 <li>Построение графа схожести по связующей переменной (например, "Работодатель ↔ Работодатель" через Навыки)</li>
               </ul>
             </li>
           </ul>
         </li>
         <li>
           <strong>Вкладка "Рекомендации"</strong>:
           <ul>
             <li><strong>Схожие узлы</strong>: Топ-N элементов, наиболее похожих на выбранный узел.</li>
             <li><strong>Соседние узлы</strong>: Топ-N прямых соседей выбранного узла.</li>
           </ul>
         </li>
       </ul>
       <hr>
       <h4>Технические особенности ⚙️</h4>
       <ul>
         <li><strong>Визуализация графов</strong>: Библиотека <strong>ipysigma</strong> на основе <strong>Sigma.js</strong> и <strong>Graphology</strong>.</li>
         <li><strong>Сетевой анализ</strong>: Расчет метрик центральности (степень, близость, посредничество) через <strong>NetworkX</strong>.</li>
         <li><strong>Рекомендательная система</strong>: Поиск схожих узлов через
          <a href="https://www.tandfonline.com/doi/full/10.1080/12460125.2024.2354585" target="_blank" rel="noopener noreferrer">обобщенную меру Жаккара</a>.</li>
       </ul>
       <hr>
       <h4>Как начать работу 🏁</h4>
       <ol>
         <li><strong>Загрузите данные</strong> через боковую панель.</li>
         <li><strong>Настройте фильтры</strong> (работодатель, навыки, специальности, регион и др.).</li>
         <li><strong>Изучите графы</strong>: Выберите переменные для одномодальных и двумодальных графов, настройте визуализацию узлов и ребер.</li>
         <li><strong>Проведите сетевой анализ</strong>: Оцените структуры сообществ, центральность и схожесть узлов.</li>
         <li><strong>Получите рекомендации</strong>: Выберите узел и получите персонализированные рекомендации на основе структуры графа.</li>
       </ol>
       <hr>
    </div>
    """
        )


# with ui.nav_panel('Инструкция', icon=icon_svg("circle-info")):
#     with ui.card(full_screen=True):
#         ui.input_action_button("rmv", "Remove UI")
#         # ui.input_selectize("specialty6", "Название специальности:",
#         #                    choices=[], multiple=True, width='400px')


with ui.nav_panel('Инструкция', icon=icon_svg("magnifying-glass")):
    with ui.navset_card_underline(id="selected_navset_card_underline2"):
        with ui.nav_panel("Загрузка и фильтрация данных"):
            ui.HTML(html_code)
            
        with ui.nav_panel("Двумодальный граф"):
            ui.HTML(html_code_2)
            
        with ui.nav_panel("Граф со-встречаемости"):
            ui.HTML(html_code_3)

        with ui.nav_panel("Граф схожести"):
            ui.HTML(html_code_4)
        
        with ui.nav_panel("Рекомендация"):
            ui.HTML(html_code_5)



# Особенности реализации:

        # with ui.div(class_="onboarding-nav"):
        #     ui.button("⬅️ Назад", id="prevBtn")
        #     ui.button("Вперед ➡️", id="nextBtn")
# Интерактивное удаление
# # @reactive.effect
# # @reactive.event(input.rmv)
# # def _():
# #     ui.remove_ui(selector="div:has(> #txt)")

# @reactive.effect
# @reactive.event(input.file)
# def _():
#     ui.remove_ui("div.form-group:has(#specialty6)")
#     ui.remove_ui("div.form-group:has(#specialty7)")


# @reactive.effect
# @reactive.event(input.file)
# def _():
#     df = processed_data()
#     df_columns = df.columns.tolist()
#     if 'Ключевые навыки' in df_columns:
#         ui.insert_ui(
#         ui.input_selectize("specialty6", "Название специальности:",
#                            choices=[], multiple=True, width='400px'),
#         selector="#rmv",
#         where="afterEnd",
#         )
#     if 'Название специальности' in df_columns:
#         ui.insert_ui(
#         ui.input_selectize("specialty7", "Название спец:",
#                            choices=[], multiple=True, width='400px'),
#         selector="#rmv",
#         where="afterEnd",
#         )




with ui.nav_panel("Данные", icon=icon_svg("table")):
    with ui.card(full_screen=True):
        ui.card_header("📖 Загруженные данные")

        @render.data_frame
        def table():
            return render.DataTable(df(), filters=True, height='625px')


# # Панель с графами
with ui.nav_panel("Сеть", icon=icon_svg('circle-nodes')):
    with ui.navset_card_underline(id="selected_navset_card_underline1"):

        with ui.nav_panel("Двумодальный граф"):
            with ui.layout_columns(col_widths=(4, 8)):
                with ui.card(full_screen=False):
                    ui.card_header("🔎 Фильтры визуализации")

                    ui.input_slider(
                        "edge_threshold_dm", "Порог силы связей:",
                        min=0, max=500, value=10, width=250
                    )

                    ui.input_selectize("node_color_dm", "Выделение цвета узла:",
                                       choices=['Модулярность', 'Модальность',
                                                'Уникальность/общность'],
                                       width=250)

                    ui.input_selectize(
                        "node_size_dm", "Метрика размера узла:",
                        choices=["Центральность по степени",
                                 "Центральность по близости", "Центральность по посредничеству"], width=250
                    )
                    ui.input_slider(
                        "node_size_range_dm", "Диапазон размера узла:",
                        min=1, max=50, value=[3, 15], width=250
                    )

                    ui.input_slider(
                        "edge_size_range_dm", "Диапазон размера ребра:",
                        min=1, max=50, value=[1, 10], width=250
                    )

                    ui.input_slider(
                        "louvain_resolution_dm", "Разрешение Louvain для модулярности:",
                        min=0, max=2, value=1, step=0.1, width=250
                    )

                    ui.input_switch("switch_shape", "Изменить форму узлов", False)

                with ui.card(full_screen=True):
                    ui.card_header("🔗 Граф")

                    @render_widget
                    def widget():
                        G = bipartite_graph()

                        if input.key_skills():
                            try:
                                skills = list(input.key_skills())
                                G = G.subgraph(
                                    skills + [n for node in skills for n in G.neighbors(node)])
                            except:
                                ui.notification_show("❌ Целевые навыки отсутствуют в выбранном графе",
                                                     type="error", duration=10
                                                     )

                        if G is None:
                            ui.notification_show(
                                "❌ Нет данных для построения графа",
                                type="error", duration=10
                            )
                            return None
                        # Выбор метрики для размера узлов

                        threshold = input.edge_threshold_dm() or 0
                        G = netfunction.filter_graph(G, threshold)

                        metric_choice = input.node_size_dm()
                        if metric_choice == "Центральность по степени":
                            metric = nx.degree_centrality(G)
                        elif metric_choice == "Центральность по близости":
                            metric = nx.closeness_centrality(G)
                        elif metric_choice == "Центральность по посредничеству":
                            metric = nx.betweenness_centrality(G)
                        else:
                            metric = nx.degree_centrality(G)
                        node_size_values = list(metric.values())

                        text_color = input.node_color_dm()
                        if text_color == 'Модулярность':
                            node_color = 'community'
                        elif text_color == 'Модальность':
                            node_color = 'bipartite'
                        elif text_color == 'Уникальность/общность':
                            node_color_dict = {}
                            for node, data in G.nodes(data=True):
                                if data.get("bipartite") == 2:  # Навыки
                                    neighbors = list(G.neighbors(node))
                                    if len(neighbors) == 1:
                                        # Уникальный навык — красный
                                        node_color_dict[node] = "#fc1717"
                                    else:
                                        # Общий навык — синий
                                        node_color_dict[node] = "#0883ef"
                                    # "#179efc"
                                else:
                                    node_color_dict[node] = "#19bb11"
                            nx.set_node_attributes(G, node_color_dict, "color")
                            node_color = "color"
                        
                        sigma_params = {"node_size": node_size_values,
                                         "node_size_range": input.node_size_range_dm() or (1, 15),
                                         "edge_size_range": input.edge_size_range_dm() or (1, 10),
                                         "node_metrics": {"community": {"name": "louvain", "resolution": input.louvain_resolution_dm() or 1}},
                                         "node_color": node_color,
                                         "hide_edges_on_move": True,
                                         "edge_size": 'weight',
                                         "hide_info_panel": True,
                                         "node_border_color_from":'node'}
                        
                        if input.switch_shape():
                            node_shape_map = {1: 'circle', 2: 'square'}
                            node_shapes = [node_shape_map[G.nodes[node].get(
                                'bipartite', 1)] for node in G.nodes]
                            sigma_params["raw_node_shape"] = node_shapes
                            sigma_params.pop("node_border_color_from", None)
                        
                        return Sigma(G, **sigma_params)

                        # return Sigma(
                        #     G,
                        #     node_size=node_size_values,
                        #     node_size_range=input.node_size_range_dm() or (1, 10),
                        #     edge_size_range=input.edge_size_range_dm() or (1, 10),
                        #     node_metrics={"community": {
                        #         "name": "louvain", "resolution": input.louvain_resolution_dm() or 1}},
                        #     node_color=node_color,
                        #     # node_border_color_from='node',
                        #     raw_node_shape=node_shapes,
                        #     hide_edges_on_move=True,
                        #     edge_size='weight',
                        #     hide_info_panel=True
                        # )

        with ui.nav_panel("Граф со-встречаемости"):
            with ui.layout_columns(col_widths=(4, 8)):
                with ui.card(full_screen=False):
                    ui.card_header("🔎 Фильтры визуализации")
                    ui.input_slider(
                        "edge_threshold_om", "Порог силы связей:",
                        min=0, max=500, value=10, width=250
                    )

                    ui.input_selectize("node_color_om", "Выделение цвета узла:",
                                       choices=['Модулярность',
                                                'Целевые узлы навыков',
                                                'Заработная плата'],  width=250)

                    ui.input_selectize(
                        "node_size_om", "Метрика размера узла:",
                        choices=["Центральность по степени",
                                 "Центральность по близости", "Центральность по посредничеству"], width=250
                    )
                    ui.input_slider(
                        "node_size_range_om", "Диапазон размера узла:",
                        min=1, max=50, value=[3, 15], width=250
                    )

                    ui.input_slider(
                        "edge_size_range_om", "Диапазон размера ребра:",
                        min=1, max=50, value=[1, 10], width=250
                    )

                    ui.input_slider(
                        "louvain_resolution_om", "Разрешение Louvain для модулярности:",
                        min=0, max=2, value=1, step=0.1, width=250
                    )
                with ui.card(full_screen=True):
                    ui.card_header("🔗 Граф")

                    @render_widget
                    def widget_semantic():
                        G = semantic_graph()

                        if input.key_skills():
                            try:
                                skills = list(input.key_skills())
                                G = G.subgraph(
                                    skills + [n for node in skills for n in G.neighbors(node)])
                            except:
                                ui.notification_show("❌ Целевые навыки отсутствуют в выбранном графе",
                                                     type="error", duration=10
                                                     )

                        if input.hard_skills():
                            try:
                                skills = list(input.hard_skills())
                                G = G.subgraph(
                                    skills + [n for node in skills for n in G.neighbors(node)])
                            except:
                                ui.notification_show("❌ Целевые профессиональные навыки отсутствуют в выбранном графе",
                                                     type="error", duration=10
                                                     )

                        if input.soft_skills():
                            try:
                                skills = list(input.soft_skills())
                                G = G.subgraph(
                                    skills + [n for node in skills for n in G.neighbors(node)])
                            except:
                                ui.notification_show("❌ Целевые надпрофессиональные навыки отсутствуют в выбранном графе",
                                                     type="error", duration=10
                                                     )

                        if G is None:
                            ui.notification_show("❌ Нет данных для построения графа",
                                                 type="error", duration=10
                                                 )
                            return None

                        threshold = input.edge_threshold_om() or 0
                        G = netfunction.filter_graph(G, threshold)
                        metric_choice = input.node_size_om()
                        if metric_choice == "Центральность по степени":
                            metric = nx.degree_centrality(G)
                        elif metric_choice == "Центральность по близости":
                            metric = nx.closeness_centrality(G)
                        elif metric_choice == "Центральность по посредничеству":
                            metric = nx.betweenness_centrality(G)
                        else:
                            metric = nx.degree_centrality(G)
                        node_size_values = list(metric.values())

                        gradient = None
                        text_color = input.node_color_om()
                        if text_color == 'Модулярность':
                            node_color = 'community'
                        elif text_color == 'Целевые узлы навыков':
                            try:
                                node_colors = []
                                for node in G.nodes():
                                    if node in skills:
                                        node_colors.append("red")
                                    else:
                                        node_colors.append("blue")
                                node_color = node_colors
                            except:
                                ui.notification_show("❌ Целевые узлы не выбраны в фильтрах",
                                                     type="error", duration=10
                                                     )
                                node_color = 'community'
                        elif text_color == 'Заработная плата':
                            data = filtered_data()
                            data = data[data['Заработная плата'] > 0]
                            data = data.explode(input.onemode_semantic())
                            median_salaries = data.groupby(input.onemode_semantic())[
                                'Заработная плата'].median().to_dict()
                            nx.set_node_attributes(
                                G, median_salaries, "median_salary")
                            node_color = "median_salary"
                            gradient = ("lightgreen", "darkgreen")

                        return Sigma(
                            G,
                            node_size=node_size_values,
                            node_size_range=input.node_size_range_om() or (3, 15),
                            edge_size_range=input.edge_size_range_om() or (1, 10),
                            node_metrics={"community": {
                                "name": "louvain", "resolution": input.louvain_resolution_om() or 1}},
                            node_color=node_color,
                            node_color_gradient=gradient,
                            hide_edges_on_move=True,
                            edge_size='weight',
                            node_border_color_from='node',
                            hide_info_panel=True
                        )

# ====== Одномодальные схожесть

        with ui.nav_panel("Граф схожести"):
            with ui.layout_columns(col_widths=(4, 8)):
                with ui.card(full_screen=False):
                    ui.card_header("🔎 Фильтры визуализации")
                    ui.input_slider(
                        "similarity_threshold", "Порог схожести:",
                        min=0, max=100, value=30, width=250
                    )

                    ui.input_selectize("node_color_sim", "Выделение цвета узла:",
                                       choices=['Модулярность',
                                                'Заработная плата'],  width=250)

                    ui.input_selectize(
                        "node_size_sim", "Метрика размера узла:",
                        choices=["Центральность по степени",
                                 "Центральность по близости", "Центральность по посредничеству"], width=250
                    )
                    ui.input_slider(
                        "node_size_range_sim", "Диапазон размера узла:",
                        min=1, max=50, value=[3, 15], width=250
                    )

                    ui.input_slider(
                        "edge_size_range_sim", "Диапазон размера ребра:",
                        min=1, max=50, value=[1, 10], width=250
                    )

                    ui.input_slider(
                        "louvain_resolution_sim", "Разрешение Louvain для модулярности:",
                        min=0, max=2, value=1, step=0.1, width=250
                    )
                with ui.card(full_screen=True):
                    ui.card_header("🔗 Граф")

                    @render_widget
                    def widget_similarity():
                        G = similarity_graph()

                        if G is None:
                            ui.notification_show("❌ Нет данных для построения графа",
                                                 type="error", duration=10
                                                 )
                            return None

                        threshold = input.similarity_threshold() / 100

                        G = netfunction.filter_graph(G, threshold)
                        metric_choice = input.node_size_sim()
                        if metric_choice == "Центральность по степени":
                            metric = nx.degree_centrality(G)
                        elif metric_choice == "Центральность по близости":
                            metric = nx.closeness_centrality(G)
                        elif metric_choice == "Центральность по посредничеству":
                            metric = nx.betweenness_centrality(G)
                        else:
                            metric = nx.degree_centrality(G)
                        node_size_values = list(metric.values())

                        gradient = None
                        text_color = input.node_color_sim()
                        if text_color == 'Модулярность':
                            node_color = 'community'
                        elif text_color == 'Заработная плата':
                            data = filtered_data()
                            data = data[data['Заработная плата'] > 0]
                            median_salaries = data.groupby(input.onemode_similarity())[
                                "Заработная плата"].median().to_dict()
                            nx.set_node_attributes(
                                G, median_salaries, "median_salary")
                            node_color = "median_salary"
                            gradient = ("lightgreen", "darkgreen")

                        return Sigma(
                            G,
                            node_size=node_size_values,
                            node_size_range=input.node_size_range_sim() or (3, 15),
                            edge_size_range=input.edge_size_range_sim() or (1, 10),
                            node_metrics={"community": {
                                "name": "louvain", "resolution": input.louvain_resolution_sim() or 1}},
                            node_color=node_color,
                            node_color_gradient=gradient,
                            hide_edges_on_move=True,
                            edge_size='weight',
                            node_border_color_from='node',
                            hide_info_panel=True
                        )

# --- Рекомендации ----


def create_bar_chart(G, node, node_type, top_n, recommendation_func, x_label, title_template):
    """
    Создает график-бар с визуализацией рекомендаций.

    :param G: Граф, в котором ищутся рекомендации.
    :param node: Выбранный узел.
    :param node_type: Тип узла ("Специальность" или "Навык").
    :param top_n: Количество наблюдений (верхних рекомендаций).
    :param recommendation_func: Функция для получения рекомендаций.
    :param x_label: Подпись для оси X.
    :param title_template: Шаблон заголовка графика (с параметрами {top_n} и {node}).
    :param error_message: Сообщение, если узел не выбран или произошла ошибка.
    :return: Объект графика Plotly.
    """
    if not node:
        return px.bar(x=["Нет выделенных узлов"], y=[0], template="plotly_white").update_layout()

    level_target = "first" if node_type == "Колонка" else "second"

    try:
        recs = recommendation_func(
            G, node, level_target=level_target, top_n=top_n)
        recs.sort(key=lambda x: x[1], reverse=False)
        nodes, similarities = zip(*recs)

        if x_label != 'Вес':
            similarities = [el * 100 for el in similarities]
    except:
        return px.bar(x=["Нет выделенных узлов"], y=[0], template="plotly_white").update_layout()

    unique_nodes = list(set(nodes))
    colors = px.colors.qualitative.G10
    color_map = {n: colors[i % len(colors)]
                 for i, n in enumerate(unique_nodes)}

    fig = px.bar(
        y=nodes,
        x=similarities,
        labels={'x': x_label, 'y': ''},
        title=title_template.format(top_n=top_n, node=node),
        color=nodes,
        template="plotly_white",
        color_discrete_map=color_map
    ).update_layout(
        showlegend=False,
        title_x=0.5,
        title_font=dict(
            size=14, color="black", weight="bold"  # Жирный шрифт
        )
    )
    return fig


with ui.nav_panel("Рекомендация", icon=icon_svg('diagram-project')):
    with ui.navset_card_underline(id="selected_navset_card_underline"):
        with ui.nav_panel("Рекомендация схожих узлов"):
            with ui.layout_columns(col_widths=(6, 6)):
                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация схожих узлов № 1")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_1", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_1", "Количество наблюдений:", 3, min=1, max=30, width="750px")
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_1():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_1", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_1", choices=choices)

                    @render_plotly
                    def recommendations_plot_1():
                        if filtered_data().empty:
                            ui.notification_show(
                                "❌ Нет данных, соответствующих выбранным фильтрам", type="error", duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_1()
                            top_n = input.obs_1()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.recommend_similar_nodes,
                            x_label='Сходство в %',
                            title_template='Топ {top_n} схожих узлов для "{node}"'
                        )

                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация схожих узлов № 2")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_2", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_2", "Количество наблюдений:", 3, min=1, max=30, width='750px')
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_2():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_2", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_2", choices=choices)

                    @render_plotly
                    def recommendations_plot_2():
                        if filtered_data().empty:
                            ui.notification_show("❌ Нет данных, соответствующих выбранным фильтрам",
                                                 type="error", duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_2()
                            top_n = input.obs_2()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.recommend_similar_nodes,
                            x_label='Сходство в %',
                            title_template='Топ {top_n} схожих узлов для "{node}"'
                        )

        with ui.nav_panel("Рекомендация соседних узлов"):
            with ui.layout_columns(col_widths=(6, 6)):
                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация соседних узлов № 1")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_3", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_3", "Количество наблюдений:", 3, min=1, max=30, width='750px')
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_3():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_3", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_3", choices=choices)

                    @render_plotly
                    def neighbor_recommendations_plot_1():
                        if filtered_data().empty:
                            ui.notification_show("❌ Нет данных, соответствующих выбранным фильтрам",
                                                 type="error",
                                                 duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_3()
                            top_n = input.obs_3()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.neighbor_recommendations,
                            x_label='Вес',
                            title_template='Топ {top_n} соседних узла "{node}"'
                        )

                # Новый блок для второй рекомендации соседних узлов
                with ui.card(full_screen=True):
                    ui.card_header("📊 Рекомендация соседних узлов № 2")

                    with ui.layout_columns(col_widths={"sm": (12, 12)}):
                        ui.input_selectize(
                            "node_4", "Выбрать узел:", choices=[], width='750px')
                        ui.input_numeric(
                            "obs_4", "Количество наблюдений:", 3, min=1, max=30, width='750px')
                    ui.hr()

                    @reactive.effect
                    def update_node_choices_4():
                        matrix = bipartite_matrix_custom()
                        if matrix.empty:
                            ui.update_selectize("node_4", choices=[])
                        else:
                            choices = list(matrix.columns) + list(matrix.index)
                            ui.update_selectize("node_4", choices=choices)

                    @render_plotly
                    def neighbor_recommendations_plot_2():
                        if filtered_data().empty:
                            ui.notification_show("❌ Нет данных, соответствующих выбранным фильтрам",
                                                 type="error",
                                                 duration=10)
                            return None

                        try:
                            G = bipartite_graph()
                            node = input.node_4()
                            top_n = input.obs_4()
                            bipartite_value = 'Колонка' if G.nodes[node]["bipartite"] == 1 else 'Строка'
                        except:
                            return None

                        return create_bar_chart(
                            G=G,
                            node=node,
                            node_type=bipartite_value,
                            top_n=top_n,
                            recommendation_func=netfunction.neighbor_recommendations,
                            x_label='Вес',
                            title_template='Топ {top_n} соседних узла для "{node}"'
                        )


# ------ Chat ---------

# welcome = '''
# 🤗 **Добро пожаловать в Networks of Opportunity!**

# Я — ваш ассистент по анализу вакансий и рынка труда.
# Могу помочь сравнить специальности, навыки и работодателей, выявить ключевые требования для специальностей, а также понять региональные особенности рынка.'''

# prompt = ChatPromptTemplate.from_template(template)


# @reactive.effect
# def update_models():
#     if input.base_url1() == "https://bothub.chat/api/v2/openai/v1":
#         models = ["gpt-3.5-turbo", "gpt-4o",
#                   "gpt-4o-mini",
#                   'o1-mini',
#                   "claude-3.7-sonnet:thinking",
#                   "claude-3.5-haiku",
#                   "deepseek-chat",
#                   "deepseek-r1",
#                   "qwen-2.5-72b-instruct",
#                   "eva-qwen-2.5-32b"]
#         ui.update_selectize("chat_model", choices=models)
#     elif input.base_url1() == "https://openrouter.ai/api/v1":
#         models = ["cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
#                   "deepseek/deepseek-chat:free",
#                   "deepseek/deepseek-r1:free",
#                   "google/gemini-2.0-flash-thinking-exp:free",
#                   'nousresearch/deephermes-3-llama-3-8b-preview:free',
#                   'qwen/qwq-32b:free']
#         ui.update_selectize("chat_model", choices=models)


# with ui.nav_panel("Чат-бот", icon=icon_svg('robot')):
#     with ui.layout_columns(col_widths=(4, 8)):
#         with ui.card(full_screen=False):
#             ui.card_header("🔎 Фильтры для чат-бота")
#             ui.input_password("chat_token", "API-токен сервиса:",
#                               width='400px',
#                               placeholder="Введите токен")
#             ui.input_selectize("chat_model", "Языковая модель:",
#                                choices=[], width='400px')
#             ui.input_selectize("base_url1", "Базовый URL-адрес сервиса:",
#                                choices=["https://bothub.chat/api/v2/openai/v1",
#                                         "https://openrouter.ai/api/v1"],
#                                selected='https://openrouter.ai/api/v1', width='400px')
#             ui.input_slider("temp", "Температура:", min=0,
#                             max=1, value=0, step=0.1, width='400px')

#         # Правая колонка: Чат-бот
#         with ui.card(full_screen=True):
#             ui.card_header("🤖 Чат-бот")
#             welcome = ui.markdown(welcome)
#             chat = ui.Chat(id="chat", messages=[welcome])
#             chat.ui(placeholder='Введите запрос...',
#                     width='min(850px, 100%)')

#         @chat.on_user_submit
#         async def process_chat():
#             user_message = chat.user_input()

#             if user_message == "Очистить чат":
#                 await chat.clear_messages()
#                 await chat.append_message_stream('Чат очищен ✅')
#                 return

#             try:
#                 # Инициализация прогресс-бара с 2 основными этапами
#                 with ui.Progress(min=0, max=5) as p:
#                     p.set(0, message="Начало обработки запроса...")

#                     # Этап 1: Работа с данными и базой
#                     p.set(1, message="Загрузка данных",
#                           detail="Подключение к векторной базе")
#                     qdrant_client = QdrantClient(
#                         url=input.qdrant_url(),
#                         api_key=input.qdrant_api_key(),
#                     )

#                     if not qdrant_client.collection_exists(collection_name=input.collection_name()):
#                         await chat.append_message_stream('Коллекция не создана ❌')
#                         return

#                     try:
#                         p.set(2, message="Загрузка данных",
#                               detail="Подготовка документов")
#                         data = processed_data()
#                         data = data[['Название региона', 'Данные', 'Опыт работы']].sample(
#                             input.filter_data(), random_state=1)
#                         loader = DataFrameLoader(
#                             data, page_content_column="Данные")
#                         documents = loader.load()
#                         splitter = RecursiveCharacterTextSplitter()
#                         split_documents = splitter.split_documents(documents)
#                     except:
#                         await chat.append_message(f'Извините, данные не загружены ❌')
#                         return

#                     p.set(3, message="Загрузка данных",
#                           detail="Обращение к векторному хранилищу")
#                     vector_store = QdrantVectorStore(
#                         client=qdrant_client,
#                         collection_name=input.collection_name(),
#                         embedding=embeddings
#                     )
#                     ensemble = create_retrievers(vector_store, split_documents)

#                     p.set(4, message="Генерация ответа",
#                           detail="Инициализация модели")
#                     model = input.chat_model()
#                     temperature = input.temp()
#                     base_url_m = input.base_url1()
#                     api_key = input.chat_token() or None

#                     try:
#                         llm = ChatOpenAI(
#                             model_name=model,
#                             temperature=temperature,
#                             max_tokens=6000,
#                             base_url=base_url_m,
#                             openai_api_key=api_key
#                         )

#                         llm_chain = (
#                             {"context": ensemble | format_docs,
#                                 "question": RunnablePassthrough()}
#                             | prompt
#                             | llm
#                             | StrOutputParser()
#                         )

#                         p.set(5, message="Генерация ответа",
#                               detail="Обработка запроса")
#                         response = llm_chain.invoke(user_message)
#                         await chat.append_message_stream(response)

#                     except:
#                         await chat.append_message('Ошибка модели, попробуйте изменить фильтры чат-бота ❌')
#                         return

#             except:
#                 await chat.append_message('Ошибка при подготовке данных: загрузите данные, настройки векторную базу данных и фильтры чат-бота ❌')

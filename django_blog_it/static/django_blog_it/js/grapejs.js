  var editor = grapesjs.init({
    height: '100%',
    showOffsets: 1,
    noticeOnUnload: 0,
    storageManager: { autoload: 0 },
    container: '#gjs',
    fromElement: true,
    allowScripts: 1,
    dragMode: 'translate',
    plugins: ['gjs-preset-webpage',
      'grapesjs-tabs',
      'grapesjs-custom-code',
      'grapesjs-touch',
      'grapesjs-parser-postcss',
      'grapesjs-tooltip',
      'grapesjs-tui-image-editor',
      'grapesjs-typed',
      'grapesjs-style-bg',
      'grapesjs-lory-slider',
      'gjs-blocks-flexbox',
      'gjs-plugin-ckeditor',
      'grapesjs-style-bg',
      'grapesjs-style-filter',
      'grapesjs-style-gradient'
    ],
    pluginsOpts: {
      'grapesjs-lory-slider': {
        sliderBlock: {
          category: 'Extra'
        }
      },
      'grapesjs-tabs': {
        tabsBlock: {
          category: 'Extra'
        }
      },
      'grapesjs-typed': {
        block: {
          category: 'Extra',
          content: {
            type: 'typed',
            'type-speed': 40,
            strings: [
              'Text row one',
              'Text row two',
              'Text row three',
            ],
          }
        }
      }
    },

  });

  editor.Panels.addButton('options',
    [{
      id: 'save-db',
      className: 'fa fa-floppy-o custom_save_button',
      command: 'save-db',
      attributes: { title: 'Save DB' }
    }]
  );

  // Add the command
  editor.Commands.add('save-db', {
    run: function(editor, sender) {
      sender && sender.set('active', 0); // turn off the button
      editor.store();

      var htmldata = editor.getHtml();
      var cssdata = editor.getCss();
      var csrftoken = $('meta[name="_token"]').attr('content');
      var status = confirm("Are you sure you want save?")
      if(status){
        $.ajax({
          type: 'POST',
          url: window.location.href,
          data: {
              "csrfmiddlewaretoken": csrftoken,
              "html": htmldata,
              "css": cssdata
            },
          success: function(data) {
            window.location.href = data.redirect_url;
          }
        });
      }
    }
  });

  function AddCustomBlock(template) {
        var blockManager = editor.BlockManager;
          block_id = "custom_block";
          blockManager.add(block_id, {
              label: 'Simple block' ,
              content: template ,
              category: 'Custom Templates',
              render: ({ el, model}) => {
                const btn = document.createElement('button');
                btn.innerHTML = 'Apply';
                btn.addEventListener('click', () =>{
                  editor.runCommand('core:canvas-clear')
                  // console.log(`${model.get('content')}`)
                  editor.setComponents(`${model.get('content')}`)
                  })
                el.appendChild(btn);
              },
          });

    }

  function AppendExistingHtml(html) {
      editor.setComponents(html);
  }

  function MakeAjaxCall() {
    var csrftoken = $('meta[name="_token"]').attr('content');
    var landing_url = $("#html").attr("landinpage-url");
    var templates_url = $("#html").attr("templates-url");
    // Append Existing Landing page
    $.ajax({
        type: 'POST',
        url: landing_url,
        data: {
            "csrfmiddlewaretoken": csrftoken,
          },
        success: function(data) {
          // console.log(data.html);
          AppendExistingHtml(data.html)
        }
      })

    // Load Templates
    $.ajax({
        type: 'POST',
        url: templates_url,
        data: {
            "csrfmiddlewaretoken": csrftoken,
          },
        success: function(template) {
          AddCustomBlock(template);
        }
      })
  }

  editor.load(res =>
    MakeAjaxCall()
  );
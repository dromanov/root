// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

$(document).ready(function() {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function() {};

  $("#messageform").on("submit", function() {
    newMessage($(this));
    return false;
  });
  $("#messageform").on("keypress", function(e) {
    if (e.keyCode == 13) {
      newMessage($(this));
      return false;
    }
    return true;
  });
  $("#message").select();
  updater.poll();

  pointers.setup_main();
});

function newMessage(form) {
  var message = form.formToDict();
  // checkpoint(["newMessage(", message])
  var disabled = form.find("input[type=submit]");
  disabled.disable();
  $.postJSON("/a/message/new", message, function(response) {
    updater.showMessage(response);
    if (message.id) {
      form.parent().remove();
    } else {
      form.find("input[type=text]").val("").select();
      disabled.enable();
    }
  });
}

function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
  args._xsrf = getCookie("_xsrf");
  $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
    success: function(response) {
      if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
      console.log("ERROR:", response);
    }
  });
};

jQuery.fn.formToDict = function() {
  var fields = this.serializeArray();
  var json = {};
  for (var i = 0; i < fields.length; i++) {
    json[fields[i].name] = fields[i].value;
  }
  if (json.next) delete json.next;
  return json;
};

jQuery.fn.disable = function() {
  this.enable(false);
  return this;
};

jQuery.fn.enable = function(opt_enable) {
  if (arguments.length && !opt_enable) {
      this.attr("disabled", "disabled");
  } else {
      this.removeAttr("disabled");
  }
  return this;
};

var updater = {
    errorSleepTime: 500,
    cursor: null,

    poll: function() {
        // checkpoint("updater.poll()")
        var args = {"_xsrf": getCookie("_xsrf")};
        if (updater.cursor) args.cursor = updater.cursor;
        $.ajax({url: "/a/message/updates", type: "POST", dataType: "text",
                data: $.param(args), success: updater.onSuccess,
                error: updater.onError});
    },

    onSuccess: function(response) {
        // checkpoint("updater.onSuccess()")
        try {
            console.log(["New message arrived:", response]);
            updater.newMessages(eval("(" + response + ")"));
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },

    newMessages: function(response) {
        // checkpoint(["updater.newMessages(", response])
        if (!response.messages) return;
        updater.cursor = response.cursor;
        var messages = response.messages;
        updater.cursor = messages[messages.length - 1].id;
        console.log(messages.length, "new messages, cursor:", updater.cursor);
        for (var i = 0; i < messages.length; i++) {
            updater.showMessage(messages[i]);
        }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};


// Interface between longpoll engine `pointers` and browser drawing.
// Takes care of creating/deleting DOM elements (cursors) and updating
// it's positions.
var users = function () {
  var cursors = {},
      spans = {},
      obj = {};

  obj.update = function (positions) {
    for (var key in cursors) {
      // Mark all fields with dirty flag
      if (cursors.hasOwnProperty(key)) {
        cursors[key].dirty = 1;
      }
    }

    for (var i=0 ; i < positions.length ; ++i) {
      var username = positions[i][0],
          position = positions[i][1];

      console.log(['...', username, positions]);

      cursors[username] = position;
      cursors[username].dirty = 0;
      if (!spans.hasOwnProperty(username)) {
        // Drawing: https://gist.github.com/rafaelportela/3026565
        spans[username] = $("<span id=" + username + ">").css({
          'position':'absolute',
          'border':'solid 2px #cc00cc',
          'border-radius':'20px',
          'width':'17px',
          'height':'17px',
        });
        $("body").append(spans[username]);
      }
      spans[username].css({
        'top': position.y - 10,
        'left': position.x - 10
      })
    }

    for (var key in cursors) {
      // Mark all fields with dirty flag
      if (cursors.hasOwnProperty(key)) {
        if (cursors[key].dirty) {
          delete cursors[key];
          delete spans[key];
        }
      }
    }
  }

  obj.set_color = function (username, color) {
    if (spans.hasOwnProperty(username)) {
      spans[username].css({
        'background-color': color
      })
    }
  }

  return obj;
}();

var pointers = {
    errorSleepTime: 500,
    version: 0,
    drop_polling: true,

    setup_main: function() {
      var args = {"_xsrf": getCookie("_xsrf")};
      $("#respawn_point").click(function () {
        console.log("Introducing new user...")
        $.ajax({
          url: "/a/pointer/new_user", type: "POST", dataType: "text",
          data: $.param(args), success: function(response) {
            console.log(["user activated", response])
            user_id = response;
            pointers.errorSleepTime = 500;
            pointers.drop_polling = false;
            window.setTimeout(pointers.poll, 0);
          },
          error: function (response) {
            console.log(['user activation failed...', response])
          }
        })
      })
      $("#logout").click(function () {
        console.log("Dropping user...")
        pointers.drop_polling = true;
        $.ajax({
          url: "/a/pointer/drop_user", type: "POST", dataType: "text",
          data: $.param(args), success: function (response) {
            console.log(['user deactivated successfully', response])
          }, error: function (response) {
            console.log(['user deactivated with error...', response])
          }
        })
      })
      $("body").mousemove(function(e) {
        // console.log(["Mouse is here:", e.pageX, e.pageY])
        if (!pointers.drop_polling) {
          args.x = e.pageX;
          args.y = e.pageY;
          $.ajax({
            url: "/a/pointer/new_position", type: "POST", dataType: "text",
            data: $.param(args), success: function(response) {
              // console.log(["mouse reported successfully", response])
            },
            error: function (response) {
              console.log(["mouse reported with error", response])
            }
          })
        }
      })
    },

    poll: function() {
      if (pointers.drop_polling) {
        return;
      }
      var args = {"_xsrf": getCookie("_xsrf")};
      args.version = pointers.version;
      $.ajax({url: "/a/pointer/updates", type: "POST", dataType: "text",
              data: $.param(args), success: pointers.onSuccess,
              error: pointers.onError});
    },

    onSuccess: function(response) {
      try {
        var res = eval("(" + response + ")");
        pointers.version = res.version;
        var positions = res.positions
        console.log(['poitions', positions])
        $("#positions").html(JSON.stringify(positions));
        users.update(positions);
      } catch (e) {
        // console.log(e);
        pointers.onError();
        return;
      }
      pointers.errorSleepTime = 500;
      window.setTimeout(pointers.poll, 0);
    },

    onError: function(response) {
      pointers.errorSleepTime *= 2;
      console.log("Pointer poll error; sleeping for", pointers.errorSleepTime, "ms");
      window.setTimeout(pointers.poll, pointers.errorSleepTime);
    },
};

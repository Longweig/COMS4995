// import {getAllFormFields} from '.util.js'

/*
    需要http.js模块和JQuery支持
*/
class Auth {

    constructor() {
        self.that = this
    }

    onRegister() {
        var ok = self.that.getUsreAuthInfo()
        if (ok) {
            var fields = getAllFormFields('register-form')
            HTTP.post('/register', fields, (msg) => {
                if (msg == 'go to index') {
                    window.location.href = '/'
                }
            }, (result) => {
                let msg = result.responseJSON
                if (msg.code == 10080) {
                    self.that.reflectToView('#email', msg.msg)
                }
                else {
                    if (msg.code == 10081) {
                        self.that.reflectToView('#nickname', msg.msg)
                    }
                    else {
                        alert('服务器内部错误')
                    }
                }
            })
        }
    }

    getUsreAuthInfo() {
        var email = $('#email').val()
        var password = $('#password').val()
        var ok = self.that.validate(email, password)
        return ok
    }

    validate(email, password) {
        var v = new Validator()
        var rightEmail = v.isEmail(email)
        var rightPassword = self.that.isCorrcetPassword(password)
        if (!rightEmail) {
            self.that.reflectToView('#email', 'Please check your email address.')
            return false
        }
        if (!rightPassword) {
            self.that.reflectToView('#password', 'Password length should be between 6 to 30 characters.')
            return false
        }
        return true
    }

    isCorrcetPassword(password) {
        var v = new Validator()
        var minPassword = v.minLength(password, 6)
        var maxpassword = v.maxLength(password, 30)
        if (minPassword && maxpassword) {
            return true
        }
        else {
            return false
        }
    }

    reflectToView(id, message) {
        $(id).tooltip({
            title: message,
            placement: 'left',
            trigger: 'manual'
        })
        $(id).tooltip('show')
    }
}


// (function init() {
//     var auth = new Auth()
//     $('#btn-submit').click(auth.onRegister)
// })()

// $(function () { $("[data-toggle='tooltip']").tooltip(); });



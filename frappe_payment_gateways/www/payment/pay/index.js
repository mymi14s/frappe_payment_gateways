const { createApp } = Vue

createApp({
  delimiters: ['[%', '%]'],
  data() {
    return {
        id: '',
        payment_data: {},
        gateway: '',
        showDiv: false
    }
  },
  methods: {
    payWithPaystack(){
        let me = this;
        let handler = PaystackPop.setup({
            key: me.payment_data.public_key, // Replace with your public key
            amount: me.payment_data.amount * 100,
            ref: me.payment_data.name+'='+me.payment_data.reference_name+'='+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
            currency: me.payment_data.currency,
            email: me.payment_data.email,
            metadata: {
                reference_doctype:me.payment_data.reference_doctype, 
                reference_name:me.payment_data.reference_name,
                log_id:me.payment_data.name},
            // label: "Optional string that replaces customer email"
            onClose: function(){
                alert('Payment Terminated.');
            },
            callback: function(response){
                response.gateway=me.payment_data.gateway;
                frappe.call({
                    type: "POST",
                    method: "frappe_payment_gateways.www.payment.pay.index.verify_transaction",
                    args:{transaction:response},
                    callback: function(r) {
                        
                    }
                });
                $('#paymentBTN').hide();
                Swal.fire(
                    'Successful',
                    'Your payment was successful, we will issue you receipt shortly.',
                    'success'
                )
            }
        });

        handler.openIframe();
    },
    getData(){
        document.addEventListener('DOMContentLoaded', () => {
            // handle the click event
            const urlParams = new URLSearchParams(window.location.search);
            const id = urlParams.get('id');
            this.id = id;
            if (!id){
                Swal.fire(
                    'Invalid',
                    'Your payment link is invalid',
                    'warning'
                )
                me.payment_data = {}
                return
            } else {
                let me =  this;
                frappe.call({
                    type: "POST",
                    method: "frappe_payment_gateways.www.payment.pay.index.get_payment_request",
                    args:{id:me.id},
                    callback: function(r) {
                        // code snippet
                        if(r.message.error){
                            Swal.fire(
                                'Error',
                                r.message.error,
                                'warning'
                            )
                            me.payment_data = {}
                            me.showDiv = false;
                        } else {
                            me.payment_data = r.message.data;
                            me.gateway = r.message.data.gateway;
                            
                            if(me.payment_data.gateway=="Paystack"){
                                $('#paymentBTN').click(()=>{
                                    me.payWithPaystack();
                                });
                            }
                            me.showDiv = true;
                        }
                    }
                });
            }
        });
        
    },
    formatCurrency(amount, currency){
        if(currency){
            return Intl.NumberFormat('en-US', {currency:currency, style:'currency'}).format(amount);
        } else {
            return Intl.NumberFormat('en-US').format(amount);
        }
    }
  },
  mounted(){
    this.getData();
  }
}).mount('#app')

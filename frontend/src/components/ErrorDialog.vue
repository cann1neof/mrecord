<template>
    <v-dialog
        v-model="dialog"
        width="30vw"
        class="px-3 py-2"
    >   
        <v-card>
            <v-card-title primary-title class="text-center">
            Ошибка
            </v-card-title>
            
            <div class="message mx-auto">
                {{err_message}}
                <br />
                Код ошибки: {{err_code}}
            </div>

            <v-card-actions>
                <mrd-button @click="close()" dark class="mx-auto"> 
                    OK
                </mrd-button>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import mrdButton from './mrdButton.vue'

export default {
    props: {
        err_code: {
            type: String,
            required: true
        },
        err_message: {
            type: String,
            required: false,
            default: ''
        },
        dialog: {
            type: Boolean,
            required: true
        }
    },
    components:{
        mrdButton,
    },
    methods: {
        close(){
            this.$emit('close')
        }
    }
}
</script>

<style scoped>
    .message{
        width: 75%;
    }
</style>
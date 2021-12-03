<template>
    <div>
        <div 
            class="viewer"
            v-if="instance"
        >
            <div 
                class="viewer-item" 
                v-for="(each, index) in instance" 
                :key="index"
            >
                <v-row>
                    <v-col cols=9>
                        <h3>{{ each.name }} </h3>
                        <p class="mb-1" > <span class="title"> Номер телефона: </span> {{ each.number }}</p>
                    </v-col>

                    <v-col cols=3>
                        <mrd-button @click="del(index)" v-if="inputer">
                            Удалить
                        </mrd-button>
                    </v-col>

                </v-row>


            </div>
        </div>
        <div class="inputer" v-if="inputer">
            <v-form ref="contactsForm">
                <v-text-field
                    v-model="name"
                    required
                    label="ФИО"
                >
                </v-text-field>

                <v-text-field
                    v-model="number"
                    required
                    label="Номер телефона"
                >
                </v-text-field>
                <div>
                    <mrd-button @click="add()" dark color="#D96906" > 
                        Добавить
                    </mrd-button>
                </div>
            </v-form>
        </div>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'

export default {
    components : { mrdButton },
    props:{
        instance : {
            type : Array,
            required : true,
        },
        inputer : {
            type : Boolean,
            required : false,
            default : true,
        }
    },
    data : ()=>({
        name : '',
        number : '',
    }),
    methods : {
        add(){
            this.$emit('add', {
                'name' : this.name,
                'number' : this.number,
            })
            this.$refs.contactsForm.reset()

        },
        del(index){
            this.$emit('del', index)
        }
    },
}
</script>

<style scoped>
.viewer-item{
    background-color: #A3B2CD;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
    width: 100%;
    font-weight: bold;
}
.title{
    font-size: 14px;
    font-weight:300;
}
</style>
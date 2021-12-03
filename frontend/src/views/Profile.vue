<template>
    <div>
        <v-row class="mx-auto">
            <v-col cols=4 :class="getCotainerClass"> 
                <h2 class="main-title">
                    Персональная информация
                </h2>
                <v-card width="50vw" class=" mx-auto pa-5" color="#013AAA" dark>
                    <h3> <span class="cont-title" > Имя: </span> {{ last_name }} {{ first_name }} {{ second_name }}</h3>
                    <h3> <span class="cont-title" > MRecord id: </span> #{{ serial_number }} </h3>
                    <h3> <span class="cont-title" > Страховой номер: </span> {{ insurance_number }} </h3>
                    <h3> <span class="cont-title" > Группа крови: </span>{{ blood_type }}</h3>
                    <mrd-button dark class="mt-2" to='/my/settings/' color="#D96906">
                        <v-icon> mdi-cog-outline </v-icon> Настройки
                    </mrd-button>
                </v-card>

                <v-card v-if="hospitals[0]" width="50vw" class=" mx-auto mt-3 pa-5" color="#013AAA" dark>
                    <span class="cont-title"> Последние посещения врача </span>
                    <hospitals-viewer :inputer="false" :instance="hospitals" ></hospitals-viewer>
                </v-card>

                <v-card v-if="recipes[0]" width="50vw" class=" mx-auto mt-3 pa-5" color="#013AAA" dark>
                    <span class="cont-title"> Лекарства и процедуры </span>
                    <recipes-viewer :inputer="false" :instance="recipes" ></recipes-viewer>
                </v-card>

                <v-card v-if="contacts[0]" width="50vw" class=" mx-auto mt-3 pa-5" color="#013AAA" dark> 
                    <span class="cont-title"> Контакты родных и близких </span>
                    <contacts-viewer :inputer="false" :instance="contacts" ></contacts-viewer>
                </v-card>

                <v-card v-if="children[0]" width="50vw" class=" mx-auto mt-3 pa-5" color="#013AAA" dark> 
                    <span class="cont-title">Родительский контроль</span>
                    <children-viewer :inputer="false" :instance="children" ></children-viewer>
                 </v-card>
                        
            </v-col>

            <v-col cols=8 v-if="illnesses[0]">
                <h2 class="main-title">
                    Заболевания и противопоказания
                </h2>
                <v-card width="100%" class="pa-5" color="#013AAA" dark>
                    <illnesses-viewer :inputer="false" :instance="illnesses" ></illnesses-viewer>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import recipesViewer from '../components/recipesViewer.vue'
import illnessesViewer from '../components/illnessesViewer.vue'
import childrenViewer from '../components/childrenViewer.vue'
import contactsViewer from '../components/contactsViewer.vue'
import hospitalsViewer from '../components/hospitalsViewer.vue'

export default{
components : {
    mrdButton,
    recipesViewer,
    illnessesViewer,
    childrenViewer,
    contactsViewer,
    hospitalsViewer,
},
data : () => ({
    first_name : '',
    second_name : '',
    last_name : '',
    serial_number : '',
    insurance_number : '',
    blood_type : '',
    illnesses : [],
    contacts : [],
    hospitals : [],
    recipes : [],
    children : [],
    showing : false,
}),
methods: {
    async validate(){
        if (!this.$store.getters.status)
            this.$router.push('/login')
        else {
            await this.getData()

            const userStore = this.$store.getters.user
            const recordStore = this.$store.getters.record
            
            this.first_name         =  userStore.first_name
            this.second_name        =  userStore.second_name
            this.last_name          =  userStore.last_name
            this.serial_number      =  recordStore.serial_number
            this.insurance_number   =  recordStore.insurance_number.toString().substr(0, 4) + ' ' + recordStore.insurance_number.toString().substr(4, 4) + ' ' + recordStore.insurance_number.toString().substr(8, 4) + ' ' + recordStore.insurance_number.toString().substr(12, 4)
            this.blood_type         =  recordStore.blood_type
            this.illnesses          =  recordStore.illnesses
            this.contacts           =  recordStore.contacts
            this.hospitals          =  recordStore.hospitals
            this.recipes            =  recordStore.recipes
            this.children           =  recordStore.children
        }
    },
    async getData(){
        const token = this.$store.getters.token
        const url = this.$store.getters.url + `octopus/${token}/r/`
        await this.$axios.get(url).then(res=>{
            const user = res.data.usr
            const record = res.data.rec
            this.$store.dispatch('createUserInfo', user)
            this.$store.dispatch('createRecordInfo', record)
        }).catch(err=>{
            if(err.response.status==401 || err.response.status==404){
                this.$emit('raise', {errCode: 'CV02', errMessage: 'Ошибка авторизации. Авторизируйтесь заново.'})
            }
        })
    }

},
watch: {
    $route(){
        this.validate()
    },
},
computed: {
    getCotainerClass(){
        if(!this.illnesses[0]){
            return { 'mx-auto' : true }
        } else {
            return { 'mx-auto' : false }
        }
    }
},
mounted(){
    this.validate()
},
}
</script>

<style scoped>
.container{
    background-color: #A3B2CD;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
}
.cont-title{
    font-size: 14px;
    font-weight: 300;
}
.block-title{
    font-weight: bolder;
    color: #505050;
}
.main-title{
    font-size: 30px;
    font-weight:900;
    color: #404040;
}
</style>
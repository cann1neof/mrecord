<template>
	<v-app 
	id="app">
		<v-app-bar
		app
		color="white"
		light
		hide-on-scroll
		height="100"
		>
		<v-row justify="space-between">
			<v-toolbar-title class="d-md-block d-none">
				<v-img 
					style="cursor:pointer;"
					src="../public/mrd-logo.png"
					width="423"
					height="96"
					@click="$router.push('/')"
				>
				</v-img>
			</v-toolbar-title>
			<div class="my-auto">
				<mrd-button class="mr-md-3" :ltl="checkwidth" dark to="/buy/" color="#D96906">Купить</mrd-button>
				<mrd-button class="mr-md-3" :ltl="checkwidth" dark to="/about/">О нас</mrd-button>
				<mrd-button class="mr-md-3" :ltl="checkwidth" dark to="/map/">Партнерам</mrd-button>
				
				<mrd-button
					dark
					to="/my/"
					:ltl="checkwidth"
					v-if="$store.getters.status"
					halfLeft=""
				>
					<v-icon>mdi-account</v-icon>
				</mrd-button>
				<mrd-button
					class="mr-md-3" 
					dark
					@click="exit()"	
					:ltl="checkwidth"
					v-if="$store.getters.status"
					color="#a11"
					halfRight=""
				>
					<v-icon>mdi-logout</v-icon>
				</mrd-button>

				<mrd-button 
					v-if="!$store.getters.status"
					class="mr-md-3" 
					dark 
					to="/login/"
					:ltl="checkwidth"
				>
					Войти
				</mrd-button>
			</div>		
		</v-row>
		</v-app-bar>
		
		<v-content>
			<v-container fluid class="mx-0 px-0 pt-0">
				<router-view @raise="raiseDialogError($event)" />
			</v-container>
		</v-content>

		<v-footer class="d-flex justify-center flex-column mt-8 mrd-footer"> 
			<v-row class="my-3">
				<v-col cols="6" >
					<v-img src="../public/mrd-black-mrecord-plus.png"> </v-img>
				</v-col>
				<v-col cols="6" >
					<v-img src="../public/mrd-black-mrecord.png"> </v-img>
				</v-col>
			</v-row>
			
			<v-row class="mt-5">
				<p>
					Developed by undefined unnamers. Moscow, 2020
				</p>
			</v-row>
		</v-footer>

		<error-dialog :dialog="errDialog" :err_code="errCode" :err_message="errMessage" @close="closeDialogError()"></error-dialog>
	</v-app>
</template>

<script>
import mrdButton from './components/mrdButton.vue'
import ErrorDialog from './components/ErrorDialog.vue'


export default {
	components:{
		mrdButton,
		ErrorDialog
	},
	data: () => ({
		errDialog: false,
		errCode: '',
		errMessage: '',
	}),
	methods: {
		raiseDialogError(event){
			this.errCode = event.errCode
			this.errMessage = event.errMessage
			this.errDialog = true
			if(event.errCode === 'CV02'){
				this.$store.dispatch('logOut')
				this.$router.push('/login')
			}
		},
		closeDialogError(){
			this.errDialog = false
		},
		exit(){
            this.$store.dispatch('logOut')
            this.$router.push('/login')
		}
	},
	computed:{
		checkwidth(){
			return window.innerWidth < 900
		}
	}
}
</script>

<style>
::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track-piece {
	background-color: #f4f4f4;
}

::-webkit-scrollbar-thumb {
    border-radius: 7px;
	background-color: #D96906;
}
</style>
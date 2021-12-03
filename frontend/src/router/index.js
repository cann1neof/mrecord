import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Purchase from '../views/Purchase.vue'
import Cart from '../views/Cart.vue'
import OnMap from '../views/OnMap.vue'
import Profile from '../views/Profile.vue'
import Settings from '../views/Settings.vue'
import AddChild from '../views/AddChild.vue'
import Child from '../views/Child.vue'
import ChildSettings from '../views/ChildSettings.vue'
import ChildMigration from '../views/ChildMigration.vue'
import NewPartner from '../views/NewPartner.vue'




Vue.use(VueRouter)

const routes = [{
		path: '/',
		component: Home,
	},
	{
		path: '/about/',
		component: About,
	},
	{
		path: '/login/',
		component: Login,
	},
	{
		path: '/register//',
		component: Register,
	},
	{
		path: '/map/',
		component: OnMap,
	},
	{
		path: '/buy/',
		component: Purchase,
	},
	{
		path: '/buy/cart/',
		component: Cart,
	},
	{
		path: '/my/',
		component: Profile,
	},
	{
		path: '/my/settings/',
		component: Settings,
	},
	{
		path: '/my/addchild/',
		component: AddChild,
	},
	{
		path: '/child/:id/',
		component: Child,
		props: true,
	},
	{
		path: '/child/:id/settings/',
		component: ChildSettings,
		props: true,
	},
	{
		path: '/child/:id/migrate/',
		component: ChildMigration,
		props: true,
	},
	{
		path: '/newpartner/',
		component: NewPartner,
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
	scrollBehavior () {
		return { x: 0, y: 0 }
	}
})

export default router
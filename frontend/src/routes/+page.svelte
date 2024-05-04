<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Advert from '$lib/advert/index.svelte';
	import Link from '$lib/button/link.svelte';

	import Tags from './home/tags.svelte';
	import Group from '$lib/group.svelte';
	import Hero from './home/hero.svelte';
	import About from './home/about.svelte';
	import Contact from './home/contact.svelte';
	import Top from './home/to_top.svelte';

	import Login from './auth/login.svelte';
	import Password from './auth/password.svelte';
	import Confirm from './auth/confirm.svelte';

	export let data;
	let { offers } = data;
	let { new_arrivals } = data;

	onMount(() => {
		if ($page.url.searchParams.has('module')) {
			let _module = {};
			switch ($page.url.searchParams.get('module')) {
				case 'password':
					_module.module = Password;
					break;
				case 'confirm':
					_module.module = Confirm;
					break;
				case 'login':
					_module.module = Login;
					break;
			}

			for (const x of ['return_url', 'token', 'message', 'email']) {
				if ($page.url.searchParams.has(x)) {
					_module[x] = $page.url.searchParams.get(x);
				}
			}

			$module = _module;
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Meta
	title="Home"
	description="Meji is your No. 1 trusted online shopping destination in Nigeria."
/>
<Log entity_type={'page'} />

<Hero />
<Advert space="home_1" placeholder />
<Tags />

<Group name="New Arrivals" items={new_arrivals}>
	<Link href="/shop?sort=latest" icon>view more</Link>
</Group>

<Group name="Offers" items={offers}>
	<Link href="/shop?sort=discount" icon>view more</Link>
</Group>

<About />
<Contact />
<Top />

<style>
</style>

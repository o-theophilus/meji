<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Advert from '$lib/advert/index.svelte';
	import Button from '$lib/button.svelte';

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
	let { tags } = data;
	let { offers } = data;
	let { new_arrivals } = data;
	let { adverts } = data;

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

<Meta title="Home" description="Home" />

<Hero />
<!-- <Advert {adverts} /> -->
<Tags {tags} />
<Group name="New Arrivals" items={new_arrivals}>
	<Button class="link small" href="/shop?sort=latest">more &gt;</Button>
</Group>
<Group name="Offers" items={offers}>
	<Button class="link small" href="/shop?sort=discount">more &gt;</Button>
</Group>
<About />
<Contact />
<Top />

<style>
</style>

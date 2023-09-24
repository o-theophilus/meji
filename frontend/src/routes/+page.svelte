<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Ads from '$lib/comp/ads.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	import Tags from './home/tags.svelte';
	import Group from '$lib/group.svelte';
	import Hero from './home/hero.svelte';
	import About from './home/about.svelte';
	import Contact from './home/contact.svelte';
	import Top from './home/to_top.svelte';

	import Login from './auth/login.svelte';
	import Password from './auth/password.svelte';
	import Confirm from './auth/confirm.svelte';

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

			if ($page.url.searchParams.has('return_url')) {
				_module.return_url = `/${$page.url.searchParams.get('return_url')}`;
			}
			if ($page.url.searchParams.has('token')) {
				_module.token = $page.url.searchParams.get('token');
			}
			if ($page.url.searchParams.has('message')) {
				_module.message = $page.url.searchParams.get('message');
			}
			if ($page.url.searchParams.has('email')) {
				_module.email = $page.url.searchParams.get('email');
			}

			$module = _module;
			window.history.replaceState(history.state, '', '/');
		}
	});
</script>

<Meta title="Home" description="Home" />

<Hero />
<Ads />
<Tags />
<Group name="New Arrivals" url="/shop?sort=latest&size=6">
	<Button class="link" href="/shop?sort=latest">
		view all <SVG type="arrow_right" size="16" />
	</Button>
</Group>
<Group name="Offers" url="/shop?sort=discount&size=6">
	<Button class="link" href="/shop?sort=discount">
		view all <SVG type="arrow_right" size="16" />
	</Button>
</Group>
<About />
<Contact />
<Top />

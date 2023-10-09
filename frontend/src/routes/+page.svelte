<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Advert from '$lib/advert/auto.svelte';
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
<!-- <Advert {adverts} /> -->
<Tags {tags} />
<Group name="New Arrivals" items={new_arrivals}>
	<svelte:fragment slot="bottom">
		<br />
		<Button class="wide" href="/shop?sort=latest">
			view all
			<span class="rotate">
				<SVG type="angle" size="10" />
			</span>
		</Button>
	</svelte:fragment>
</Group>
<Group name="Offers" items={offers}>
	<svelte:fragment slot="bottom">
		<br />
		<Button class="wide" href="/shop?sort=discount">
			view all
			<span class="rotate">
				<SVG type="angle" size="10" />
			</span>
		</Button>
	</svelte:fragment>
</Group>
<About />
<Contact />
<Top />

<style>
	.rotate {
		transform: rotate(180deg);
	}
</style>

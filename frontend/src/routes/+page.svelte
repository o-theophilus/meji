<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { module } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Meta from '$lib/comp/meta.svelte';
	import Ads from '$lib/comp/ads.svelte';
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from '$lib/comp/item.svelte';
	import Button from '$lib/comp/button.svelte';

	import Category from './page.cate.svelte';
	import Hero from './page.hero.svelte';
	import About from './page.about.svelte';
	import Top from './page.to_top.svelte';

	import Login from '$lib/module/login.svelte';
	import Password from '$lib/module/change_password.svelte';
	import Email from '$lib/module/change_email.svelte';
	import Confirm from '$lib/module/confirm.svelte';

	export let data;
	let { group } = data;
	let { categories } = data;
	let { ads } = data;

	onMount(() => {
		if ($page.url.searchParams.get('module') == 'login') {
			let return_url = `/${$page.url.searchParams.get('return_url')}`;
			window.history.replaceState('', '', '/');
			$module = {
				module: Login,
				data: {
					message: 'Please login to access your profile',
					return_url
				}
			};
		}

		let _module = $page.url.searchParams.get('module');
		if (_module && ['password', 'email', 'confirm'].includes(_module)) {
			let token = $page.url.searchParams.get('token');
			window.history.replaceState('', '', '/');

			let mod;
			if (_module == 'password') {
				mod = Password;
			} else if (_module == 'email') {
				mod = Email;
			} else if (_module == 'confirm') {
				mod = Confirm;
			}
			$module = {
				module: mod,
				data: {
					token
				}
			};
		}
	});
</script>

<Meta title="Home" description="Home" />

<section>
	<Hero />
	<Ads {ads} />
	<Category {categories} />

	{#each group as x}
		{#if x.items.length > 0}
			<div id={x.name.toLowerCase().replace(' ', '_')} />
			<Card>
				<Title title={x.name}>
					<Button
						class="tiny link"
						name="view all >"
						on:click={() => {
							$state['shop'].order = x.query.order;
							goto(`/shop`);
						}}
					/>
				</Title>
				<Body grid>
					{#each x.items as item (item.key)}
						<Item {item} />
					{/each}
				</Body>
			</Card>
		{/if}
	{/each}

	<div id="about" />
	<About />
</section>
<Top />

<style>
	section {
		display: grid;
		gap: var(--gap2);
	}
</style>

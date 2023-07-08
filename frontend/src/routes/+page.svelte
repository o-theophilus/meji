<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { module } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Meta from '$lib/meta.svelte';
	import Ads from '$lib/comp/ads.svelte';
	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/comp/button.svelte';

	import Category from './page.cate.svelte';
	import Hero from './page.hero.svelte';
	import About from './page.about.svelte';
	import Top from './page.to_top.svelte';

	import Login from './auth/login.svelte';
	import Password from './profile/setting/password.svelte';
	import Email from './profile/email.svelte';
	import Confirm from './auth/confirm.svelte';

	export let data;
	let { group } = data;
	let { categories } = data;
	let { ads } = data;

	onMount(() => {
		if ($page.url.searchParams.has('module')) {
			let _module = {};
			switch ($page.url.searchParams.get('module')) {
				case 'password':
					_module.module = Password;
					break;
				case 'email':
					_module.module = Email;
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

<section>
	<Hero />
	<Ads {ads} />
	<Category {categories} />

	{#if group}
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
	{/if}

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

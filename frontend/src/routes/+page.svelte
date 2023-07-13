<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { module } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Meta from '$lib/meta.svelte';
	import Ads from '$lib/comp/ads.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/button.svelte';

	import Tag from './page.tag.svelte';
	import Tag_All from './page.tagall.svelte';
	import Hero from './page.hero.svelte';
	import About from './page.about.svelte';
	import Top from './page.to_top.svelte';

	import Login from './auth/login.svelte';
	import Password from './auth/password.svelte';
	import Confirm from './auth/confirm.svelte';

	export let data;
	let { group } = data;
	let { tags } = data;
	let { ads } = data;

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
<Ads {ads} />

{#if tags.length > 0}
	<div id="tag" />
	<Card>
		<div class="title">
			tags
			<Button
				class="link"
				name="view all >"
				on:click={() => {
					$module = {
						module: Tag_All,
						tags
					};
				}}
			/>
		</div>

		<div class="items" class:grid={true}>
			{#each tags.slice(0, 6) as tag}
				<Tag {tag} />
			{/each}
		</div>
	</Card>
{/if}

{#if group}
	{#each group as x}
		{#if x.items.length > 0}
			<div id={x.name.toLowerCase().replace(' ', '_')} />
			<Card>
				<div class="title">
					{x.name}
					<Button
						class="link"
						name="view all >"
						on:click={() => {
							$state['shop'].order = x.query.order;
							goto(`/shop`);
						}}
					/>
				</div>

				<div class="items" class:grid={true}>
					{#each x.items as item (item.key)}
						<Item {item} />
					{/each}
				</div>
			</Card>
		{/if}
	{/each}
{/if}

<div id="about" />
<About />

<Top />

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}

	.items {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: 1fr;

		margin-top: var(--sp4);
		color: var(--ac1);
	}
	.grid {
		grid-template-columns: repeat(2, 1fr);
	}
	@media screen and (min-width: 700px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
	@media screen and (min-width: 1000px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>

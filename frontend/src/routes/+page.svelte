<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { module, user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Ads from '$lib/comp/ads.svelte';
	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/button.svelte';

	import Tag from './home/tag.svelte';
	import Tag_All from './home/tag_all.svelte';
	import Hero from './home/hero.svelte';
	import About from './home/about.svelte';
	import Top from './home/to_top.svelte';

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
			Tags
			<Button
				class="link"
				on:click={() => {
					$module = {
						module: Tag_All,
						tags
					};
				}}
			>
				view all <SVG type="arrow_right" size="16" />
			</Button>
		</div>

		<div class="item_area">
			{#each tags.slice(0, 6) as tag}
				<Tag {tag} />
			{/each}
		</div>
	</Card>
{/if}

{#each group as x}
	{#if x.items.length > 0}
		<div id={x.name.toLowerCase().replace(' ', '_')} />
		<Card>
			<div class="title">
				{x.name}
				<Button class="link" href="/shop">view all <SVG type="arrow_right" size="16" /></Button>
			</div>

			<div class="item_area" class:list={$user.setting.item_view == 'list'}>
				{#each x.items as item (item.key)}
					<Item {item} />
				{/each}
			</div>
		</Card>
	{/if}
{/each}

<div id="about" />
<About />

<Top />

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}
	.title {
		fill: currentColor;
	}
</style>

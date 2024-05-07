<script>
	import { page } from '$app/stores';
	import { user as me, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Title from '$lib/title.svelte';

	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Logout from '../auth/logout.svelte';

	import Photo from './photo.svelte';
	import Name from './name.svelte';
	import Email from './email.svelte';
	import Phone from './phone.svelte';
	import Address from './address.svelte';
	import Account from './account.svelte';
	import SVG from '$lib/svg.svelte';
	import Search from '$lib/search.svelte';
	import Center from '$lib/center.svelte';
	import Permission from './permission.svelte';

	export let data;
	$: user = data.user;
	let { permissions } = data;

	let edit_mode = false;

	$: if ($portal) {
		if ($portal.type == 'user') {
			user = $portal.data;
		} else if ($portal.type == 'photo' && user.key == $me.key) {
			$me.photo = $portal.data;
		}
		$portal = '';
	}
</script>

<Meta title={user?.name || data.error} description={user?.name || data.error} />
{#if user}
	{#key user.key}
		<Log
			action={'viewed'}
			entity_key={user.key == $me.key ? null : user.key}
			entity_type={'user'}
		/>
	{/key}
{:else if data.error}
	{#key `${$page.url.pathname}${$page.url.search}`}
		<Log
			action={'viewed'}
			entity_key={$page.url.searchParams.get('search')}
			entity_type={'user'}
			status={data.status}
		/>
	{/key}
{/if}

<Center>
	<Title>
		User Details
		<svelte:fragment slot="right">
			{#if user && user.key == $me.key}
				<Toggle
					active={edit_mode}
					state_2="edit"
					on:click={() => {
						edit_mode = !edit_mode;
					}}
				/>
			{/if}
		</svelte:fragment>
	</Title>
</Center>

<Card>
	{#if $me.permissions.includes('user:view')}
		<Search placeholder="Search for User by  Email or Key" />
		<br />
	{/if}

	{#if data.error}
		<span class="error">
			{data.error}
		</span>
	{:else}
		<div class="block">
			<div class="photo">
				<Photo {user} {edit_mode} />
			</div>

			<div>
				<Name {user} {edit_mode} />
				<br />
				<div class="details">
					{#if user.key != $me.key}
						<span class="bold"> Status: </span>
						{user.status}
						<div />
					{/if}
					<Phone {user} {edit_mode} />
					<Email {user} {edit_mode} />
					<Address {user} {edit_mode} />
				</div>
				<br />
				<Account {user} />

				{#if user.key == $me.key}
					<br />
					<hr />
					<br />

					<div class="row">
						{#if user.permissions.length != 0}
							<Link href="/admin">Admin</Link> |
						{/if}
						<Link href="/orders">Orders</Link>
						{#if $me.permissions.includes('log:view')}
							| <Link href="/log">Logs</Link>
						{/if}
					</div>

					<br />
					<hr />
					<br />

					<div class="row">
						{#if edit_mode}
							<Button href="/profile/setting">
								<SVG icon="setting" size="12" />
								Setting
							</Button>
						{/if}
						<Logout />
					</div>
				{:else if $me.permissions.includes('log:view')}
					<br />
					<hr />
					<br />

					<Link href="/log?{new URLSearchParams(`search=${user.email}:all:all:`).toString()}">
						view logs
					</Link>
				{/if}
			</div>
		</div>
	{/if}
</Card>

{#if user && user.key != $me.key && user.status == 'confirmed' && $me.permissions.includes('user:set_permission')}
	<Permission {user} {permissions} />
{/if}

<style>
	.block {
		gap: var(--sp3);
		display: flex;
		flex-direction: column;
	}
	.block > div {
		width: 100%;
	}

	.bold {
		font-weight: 700;
	}

	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.details {
		display: grid;
		gap: 0 var(--sp2);
		grid-template-columns: max-content auto min-content;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
	}
</style>

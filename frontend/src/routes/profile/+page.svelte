<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user as me, module, portal, set_state } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';

	import Button from '$lib/button.svelte';
	import Logout from '../auth/logout.svelte';

	import Photo from './photo.svelte';
	import Edit_Name from './_name.svelte';
	import Edit_Email from './_email.svelte';
	import Edit_Phone from './_phone.svelte';
	import Edit_Address from './_address.svelte';
	import Add_Voucher from './_voucher.svelte';
	import SVG from '$lib/svg.svelte';
	import Search from '$lib/search.svelte';
	import Center from '$lib/center.svelte';
	import Permission from './permission.svelte';

	export let data;
	$: user = data.user;
	let { permissions } = data;

	let edit_mode = false;
	let page_name = 'profile';

	$: if ($portal && $portal.type == 'user') {
		user = $portal.data;
		$portal = '';
	}

	let search = '';
	let _search = '';
	const submit = () => {
		if (_search != search) {
			_search = `${search}`;
			set_state(page_name, 'search', search);
		}
	};
	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}
	});
</script>

<Meta title={user?.name || data.error} description={user?.name || data.error} />
<!-- TODO: how best to log this -->
<!-- <Log entity_type={'page'} /> -->

<Center>
	<br />
	<div class="ctitle">
		User Details
		{#if user && user.key == $me.key}
			<Button
				class="outline"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			>
				<SVG type="edit" size="10" />
				Edit: {edit_mode ? 'On' : 'Off'}
			</Button>
		{/if}
	</div>
</Center>

<Card>
	{#if $me.permissions.includes('user:view')}
		<div class="line">
			<Search
				placeholder="Search for User by  Email or Key"
				bind:search
				on:ok={() => {
					submit();
				}}
				on:clear={() => {
					search = '';
					submit();
				}}
			/>
			<Button class="primary" on:click={submit} disabled={search == _search}>Search</Button>
		</div>

		<br />
	{/if}

	{#if data.error}
		<span class="error">
			{data.error}
		</span>
	{:else}
		<div class="block">
			<div class="photo">
				<Photo {edit_mode} />
			</div>

			<div>
				<div class="horizontal space">
					<span class="name">
						{user.name}
					</span>
					{#if edit_mode}
						<Button
							class="round"
							tooltip="Edit Name"
							on:click={() => {
								$module = {
									module: Edit_Name,
									user: user
								};
							}}
						>
							<SVG type="edit" size="10" />
						</Button>
					{/if}
				</div>

				<br />

				<div class="details">
					{#if user.key != $me.key}
						<span class="bold"> Status: </span>
						{user.status}
						<div />
					{/if}

					<span class="bold"> Phone: </span>
					{#if user.phone}
						{user.phone}
					{:else}
						No Phone
					{/if}
					{#if edit_mode}
						<Button
							class="round"
							tooltip="Edit Phone Number"
							on:click={() => {
								$module = {
									module: Edit_Phone,
									user: user
								};
							}}
						>
							<SVG type="edit" size="10" />
						</Button>
					{:else}
						<div />
					{/if}

					<span class="bold"> Email: </span>
					{user.email}
					{#if edit_mode}
						<Button
							class="round"
							tooltip="Edit Email"
							on:click={() => {
								$module = {
									module: Edit_Email,
									user: user
								};
							}}
						>
							<SVG type="edit" size="10" />
						</Button>
					{:else}
						<div />
					{/if}

					<span class="bold"> Address: </span>
					{#if user.line && user.local_area && user.state && user.country && user.postal_code}
						{user.line}, {user.local_area}, {user.state}, {user.country}.
					{:else}
						No Address
					{/if}

					{#if edit_mode}
						<Button
							class="round"
							tooltip="Edit Address"
							on:click={() => {
								$module = {
									module: Edit_Address,
									user: user
								};
							}}
						>
							<SVG type="edit" size="10" />
						</Button>
					{:else}
						<div />
					{/if}

					{#if user.line && user.local_area && user.state && user.country && user.postal_code}
						<span class="bold"> Postal Code: </span>
						{user.postal_code}
					{/if}
				</div>

				<br />

				<div class="horizontal">
					<p>
						<span class="bold"> Account: </span>
						<br />
						Balance:

						{#if user.account_balance != '#'}
							₦{user.account_balance.toLocaleString()}
						{:else}
							{user.account_balance}##
						{/if}
					</p>

					{#if user.key == $me.key}
						<Button
							on:click={() => {
								$module = {
									module: Add_Voucher
								};
							}}
						>
							Add Voucher
						</Button>
						<Button href="/profile/transaction">Transaction</Button>
					{/if}
				</div>

				{#if user.key == $me.key}
					<br />

					<div class="horizontal">
						{#if user.permissions.length != 0}
							<Button href="/admin">Admin</Button>
						{/if}

						<Button href="/orders">Orders</Button>

						{#if $me.permissions.includes('log:view')}
							<Button href="/log">Logs</Button>
						{/if}
					</div>

					<br />
					<hr />
					<br />

					<div class="horizontal">
						{#if edit_mode}
							<Button href="/profile/setting">
								<SVG type="setting" size="12" />
								Setting
							</Button>
						{/if}
						<Logout />
					</div>
				{/if}

				{#if user.key != $me.key && $me.permissions.includes('log:view')}
					<br />
					<Button
						class="link small"
						href="/log?{new URLSearchParams(`search=${user.email}:all:all:all`).toString()}"
						>view log &gt;</Button
					>
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

	.name {
		font-weight: 900;
		color: var(--ac1);
	}
	.bold {
		font-weight: 700;
	}

	.horizontal {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}
	.space {
		justify-content: space-between;
	}

	.details {
		display: grid;
		gap: 0 var(--sp2);
		grid-template-columns: max-content auto min-content;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
	}
</style>

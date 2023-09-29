<script>
	import { user as me, module, portal } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';

	import Button from '$lib/button.svelte';
	import Logout from '../auth/logout.svelte';

	import Photo from './photo.svelte';
	import Edit_Name from './_name.svelte';
	import Edit_Email from './_email.svelte';
	import Edit_Phone from './_phone.svelte';
	import Edit_Address from './_address.svelte';
	import Add_Voucher from './_voucher.svelte';
	import SVG from '$lib/svg.svelte';
	import Search from './search.svelte';

	export let data;
	let user = data.user || $me;
	let edit_mode = false;
	let page_name = 'profile';

	$: if ($portal && $portal.type == 'user') {
		user = $portal.data;
		$portal = '';
	}
</script>

<Meta title={user.name} description={user.name} />

{#if user.roles.includes('admin')}
	<Search {page_name} />
{/if}

<Card>
	{#if data.error}
		<span class="error">
			{data.error}
		</span>
		<br />
		<br />
	{/if}
	<div class="title">
		User Details
		{#if user.key == $me.key}
			<Button
				class="small"
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			>
				<SVG type="edit" size="12" />
				Edit Mode: {edit_mode ? 'On' : 'Off'}
			</Button>
		{/if}
	</div>

	<div class="block">
		<div class="photo">
			<Photo {edit_mode} />
		</div>

		<div>
			<div class="horizontal space">
				<b>
					{user.name}
				</b>
				{#if edit_mode}
					<Button
						class="small round"
						tooltip="Edit Name"
						on:click={() => {
							$module = {
								module: Edit_Name,
								user: user
							};
						}}
					>
						<SVG type="edit" size="12" />
					</Button>
				{/if}
			</div>

			<br />

			<div class="details">
				<span class="bold"> Phone: </span>
				{#if user.phone}
					{user.phone}
				{:else}
					No Phone
				{/if}
				{#if edit_mode}
					<Button
						class="small round"
						tooltip="Edit Phone Number"
						on:click={() => {
							$module = {
								module: Edit_Phone,
								user: user
							};
						}}
					>
						<SVG type="edit" size="12" />
					</Button>
				{:else}
					<div />
				{/if}

				<span class="bold"> Email: </span>
				{user.email}
				{#if edit_mode}
					<Button
						class="small round"
						tooltip="Edit Email"
						on:click={() => {
							$module = {
								module: Edit_Email,
								user: user
							};
						}}
					>
						<SVG type="edit" size="12" />
					</Button>
				{:else}
					<div />
				{/if}

				<span class="bold"> Address: </span>
				{#if user.address.line && user.address.local_area && user.address.state && user.address.country && user.address.postal_code}
					{user.address.line}, {user.address.local_area}, {user.address.state}, {user.address
						.country}.
				{:else}
					No Address
				{/if}

				{#if edit_mode}
					<Button
						class="small round"
						tooltip="Edit Address"
						on:click={() => {
							$module = {
								module: Edit_Address,
								user: user
							};
						}}
					>
						<SVG type="edit" size="12" />
					</Button>
				{:else}
					<div />
				{/if}

				{#if user.address.line && user.address.local_area && user.address.state && user.address.country && user.address.postal_code}
					<span class="bold"> Postal Code: </span>
					{user.address.postal_code}
				{/if}
			</div>

			<br />

			<div class="horizontal">
				<p>
					<span class="bold"> Account: </span>
					<br />
					Balance: ₦{user.acc_balance.toLocaleString()}
				</p>
				<Button
					class="small"
					on:click={() => {
						$module = {
							module: Add_Voucher
						};
					}}
				>
					Add Voucher
				</Button>
			</div>

			<br />

			<div class="horizontal">
				{#if user.key == $me.key}
					<Button class="small" href="/orders">Orders</Button>
					{#if user.roles.includes('admin')}
						<Button class="small" href="/admin">Admin</Button>
					{/if}
					{#if edit_mode}
						<Button class="small" href="/profile/setting">
							<SVG type="setting" size="12" />
							Setting
						</Button>
					{/if}
					<Logout />
				{/if}
			</div>
		</div>
	</div>
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.block {
		gap: var(--sp3);
		display: flex;
		flex-direction: column;

		margin-top: var(--sp2);
	}
	.block > div {
		width: 100%;
	}

	.bold {
		font-weight: 500;
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

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
	}
</style>

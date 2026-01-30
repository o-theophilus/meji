<script>
	import { page } from '$app/state';

	import { app, module, page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Meta, Icon, Avatar, Log } from '$lib/macro';
	import { RoundButton, Button, LinkArrow, Toggle } from '$lib/button';

	import Photo from './_photo.svelte';
	import Name from './_name.svelte';
	import Phone from './_phone.svelte';
	import Username from './_username.svelte';
	import Email from './email/1_email.svelte';
	import Password from './password/1_email.svelte';
	import Delete from './delete/form.svelte';
	import Access from './access/form.svelte';
	import Action from './_admin_action.svelte';
	import Block from './_block.svelte';
	import { onMount } from 'svelte';

	let { data } = $props();
	let user = $derived(data.user);
	let edit_mode = $state(false);

	const update = (data) => {
		user = data;

		if (user.key == app.user.key) {
			app.user = data;
		}
	};
</script>

<Meta title={user.name} />
<Log action={'viewed'} entity_key={user.key} entity_type={'user'} />

<Content --content-background-color="var(--bg)">
	<div class="line">
		<div class="page_title">Profile</div>
		{#if app.login && user.status == 'active' && (user.key == app.user.key || app.user.access.some( (x) => ['user:set_access', 'user:reset_name', 'user:reset_username', 'user:reset_photo', 'block:block', 'block:unblock'].includes(x) ))}
			<Toggle
				state_2="edit"
				active={edit_mode}
				onclick={() => {
					edit_mode = !edit_mode;
				}}
			/>
		{/if}
	</div>

	<br /><br /><br />

	<div class="line center">
		<Avatar name={user.name} photo={user.photo} size="120" --avatar-border-radius="50%" />

		{#if edit_mode && user.key == app.user.key}
			<RoundButton
				icon="square-pen"
				onclick={() => {
					module.open(Photo, {
						key: user.key,
						name: user.name,
						photo: user.photo,
						type: 'user',
						slug: '/user/photo',
						update
					});
				}}
			/>
		{/if}
	</div>

	<br />

	<div class="line center">
		<Icon icon="user" />
		<div class="name">
			{user.name}
		</div>
		{#if edit_mode && user.key == app.user.key}
			<RoundButton icon="square-pen" onclick={() => module.open(Name, { update })} />
		{/if}
	</div>

	<div class="line center">
		<Icon icon="mail" />
		{user.email}
		{#if edit_mode && user.key == app.user.key}
			<RoundButton icon="square-pen" onclick={() => module.open(Email, { update })} />
		{/if}
	</div>

	{#if (edit_mode && user.key == app.user.key) || user.phone}
		<div class="line center">
			<Icon icon="phone" />
			{user.phone || 'None'}
			{#if edit_mode && user.key == app.user.key}
				<RoundButton icon="square-pen" onclick={() => module.open(Phone, { update })} />
			{/if}
		</div>
	{/if}

	{#if edit_mode && user.key == app.user.key}
		<div class="line center">
			<Icon icon="at-sign" />
			{user.username}
			<RoundButton icon="square-pen" onclick={() => module.open(Username, { update })} />
		</div>

		<div class="line center">
			<Icon icon="key-round" />
			********
			<RoundButton icon="square-pen" onclick={() => module.open(Password)} />
		</div>
	{/if}

	{#if edit_mode}
		<br />
		<div class="line center wrap">
			{#if user.key == app.user.key}
				<Button onclick={() => module.open(Delete)}>
					<Icon icon="trash-2" />
					Delete Account
				</Button>
			{:else}
				{#if app.user.access.includes('user:set_access')}
					<Button onclick={() => module.open(Access, { user, update })}>Access</Button>
				{/if}

				{#if app.user.access.some( (x) => ['user:reset_name', 'user:reset_username', 'user:reset_photo'].includes(x) )}
					<Button onclick={() => module.open(Action, { ...user, update })}>Reset</Button>
				{/if}

				{#if app.user.access.includes('block:block')}
					<Button
						icon="lock-keyhole"
						disabled={user.blocked}
						onclick={() => module.open(Block, { user, update })}
					>
						Block{#if user.blocked}ed{/if}
					</Button>
				{/if}
			{/if}
		</div>
	{/if}
	<br /><br /><br />

	<div class="pad">
		<LinkArrow --link-font-size="0.8rem" href="/orders">Orders</LinkArrow>
	</div>
	{#if app.user.access.includes('log:view')}
		<hr />
		<div class="pad">
			<LinkArrow
				--link-font-size="0.8rem"
				onclick={() => page_state.goto('log', { u_search: user.key })}
			>
				View Logs
			</LinkArrow>
		</div>
	{/if}
</Content>

<style>
	.name {
		font-weight: 800;
		color: var(--ft1);
		font-size: 1.2rem;
	}
	.center {
		text-align: center;
		justify-content: center;
	}

	.pad,
	hr {
		margin: 16px 0;
	}
</style>

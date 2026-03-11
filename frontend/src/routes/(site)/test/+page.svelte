<script>
	import { Switch } from '$lib/button';
	import { IG, Input } from '$lib/input';
	import Pagination from '$lib/input/pagination.svelte';
	import { Content } from '$lib/layout';

	let show_password = $state();
</script>

<Content>
	<Switch list={['one', 'two', 'three']}></Switch>
	<Switch list={['one', 'two', 'three']}></Switch>
	<IG disabled name="hello 1" error="hello" type="text" icon="heart" placeholder="hello"></IG>
	<IG disabled name="hello 2" type="textarea" placeholder="hello"></IG>
	<IG disabled name="hello 3" type="code" placeholder="hello"></IG>
	<IG  name="hello 4" value="6" type="number"></IG>

	<Pagination value="3" total_page="5"></Pagination>
	<IG disabled name="hello 5" type="rating" placeholder="hello"></IG>
	<IG disabled name="hello 6" type="date" placeholder="hello"></IG>
	<IG disabled name="hello 7" bind:show_password type="password" placeholder="password"></IG>
	<IG disabled name="hello 8" bind:show_password type="password++" placeholder="password"></IG>

	<Input disabled --input-margin-top="16px" type="text" icon="heart" placeholder="hello"></Input>
	<Input disabled --input-margin-top="16px" type="textarea" placeholder="hello"></Input>
	<Input disabled --input-margin-top="16px" type="code" placeholder="hello"></Input>
	<Input disabled --input-margin-top="16px" type="number" placeholder="hello"></Input>
	<Input disabled --input-margin-top="16px" type="rating" placeholder="hello"></Input>
	<Input disabled --input-margin-top="16px" type="date" placeholder="hello"></Input>
	<Input disabled --input-margin-top="16px" type="password" placeholder="password"></Input>
	<Input disabled --input-margin-top="16px" type="password++" placeholder="password"></Input>
</Content>
